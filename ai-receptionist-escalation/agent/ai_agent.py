"""
LiveKit AI Receptionist Agent
Handles incoming calls, checks knowledge base, and escalates unknown questions
"""

import asyncio
import os
from livekit import agents
from livekit.agents import (
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import openai, silero
try:
    # Prefer Deepgram when available (for STT/TTS)
    from livekit.plugins import deepgram
except Exception:
    deepgram = None
from dotenv import load_dotenv

from agent.help_request import HelpRequestService
from agent.knowledge_base import KnowledgeBaseManager

# Load environment variables
load_dotenv('.env.local')

# Initialize services (lazy initialization to handle errors gracefully)
help_service = None
kb_manager = None

def get_help_service():
    """Lazy initialization of help service"""
    global help_service
    if help_service is None:
        try:
            help_service = HelpRequestService()
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize help service: {e}")
            help_service = None
    return help_service

def get_kb_manager():
    """Lazy initialization of KB manager"""
    global kb_manager
    if kb_manager is None:
        try:
            kb_manager = KnowledgeBaseManager()
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize KB manager: {e}")
            kb_manager = None
    return kb_manager

# Salon business context prompt
SALON_PROMPT = """You are a friendly and professional AI receptionist for a hair salon called "Glamour Cuts".

Business Information:
- Hours: Monday-Saturday 9am-7pm, Sunday 10am-6pm
- Services: Haircuts, coloring, highlights, perms, styling, keratin treatments
- Location: Downtown area, street parking available
- Booking: Appointments preferred, walk-ins welcome
- Contact: Phone or online booking available

Your role:
1. Greet callers warmly and professionally
2. Answer questions about services, hours, pricing, and booking
3. If you don't know an answer, you must escalate it by calling the request_help function
4. Before answering questions about specific services or pricing, check your knowledge base
5. Be helpful, concise, and friendly

Important: You have access to a knowledge base. For any question about specific services, pricing, or treatments that you're not sure about, 
you should first check the knowledge base. If the information is not found, you must call the request_help function.
"""


def extract_caller_info(ctx: JobContext) -> str:
    """Extract caller phone number from room metadata or generate default"""
    # In real implementation, this would come from LiveKit room metadata
    # For now, we'll use a default or generate from participant
    if ctx.room and hasattr(ctx.room, 'name'):
        room_name = ctx.room.name
        if room_name and 'caller_' in room_name:
            parts = room_name.split('caller_')
            if len(parts) > 1:
                return f"+{parts[-1]}"
    
    # Default for testing
    return os.getenv('DEFAULT_CALLER_PHONE', '+1234567890')


def prewarm(ctx: JobContext):
    """Pre-initialize services"""
    print("🔥 Pre-warming agent services...")
    try:
        get_help_service()
        get_kb_manager()
        print("✅ Services initialized successfully")
    except Exception as e:
        print(f"⚠️ Warning during prewarm: {e}")


async def entrypoint(ctx: JobContext):
    """Main entry point for LiveKit agent"""
    print(f"📞 Incoming call in room: {ctx.room.name if hasattr(ctx.room, 'name') else 'unknown'}")
    
    # Connect to room first
    await ctx.connect()
    print("✅ Connected to room")
    
    # Wait for participant to connect
    await ctx.wait_for_participant()
    print("✅ Participant connected")
    
    # Get caller phone (for help requests)
    caller_phone = extract_caller_info(ctx)
    print(f"📱 Caller: {caller_phone}")
    
    # Initialize services
    kb_mgr = get_kb_manager()
    help_svc = get_help_service()
    
    # Create function tools for LLM
    def check_knowledge_base(question: str) -> str:
        """Check if we have information about the caller's question in our knowledge base.
        
        Args:
            question: The question the caller is asking
            
        Returns:
            The answer if found, or empty string if not found
        """
        if not kb_mgr:
            return ""
        try:
            answer = kb_mgr.check_knowledge(question)
            if answer:
                print(f"✅ Found answer in KB for: '{question}'")
                return answer
            else:
                print(f"❌ No answer found in KB for: '{question}'")
                return ""
        except Exception as e:
            print(f"⚠️ Error checking KB: {e}")
            return ""
    
    def request_help(question: str) -> str:
        """Request help from supervisor when you don't know the answer to a question.
        
        Call this function when the caller asks something you cannot answer from your knowledge base.
        
        Args:
            question: The question the caller is asking that you cannot answer
            
        Returns:
            Confirmation message
        """
        if not help_svc:
            print("⚠️ Help service not available, cannot create request")
            return "I apologize, but I'm having trouble processing your request right now."
        
        try:
            print(f"🆘 Requesting help for question: '{question}'")
            request_id = help_svc.create_request(question, caller_phone)
            print(f"✅ Help request created: {request_id}")
            return "Let me check with my supervisor and get back to you on that."
        except Exception as e:
            print(f"❌ Error creating help request: {e}")
            return "I apologize, but I'm having trouble processing your request right now."
    
    # Initialize voice components (prefer Deepgram if configured)
    vad = silero.VAD.load()
    use_deepgram = bool(os.getenv("DEEPGRAM_API_KEY")) and deepgram is not None

    llm_instance = None

    if use_deepgram:
        print("🟦 Using Deepgram STT/TTS")
        stt = deepgram.STT(model="nova-2")
        try:
            tts = deepgram.TTS(model="aura-asteria-en")
        except TypeError:
            tts = deepgram.TTS()

        # LLM selection (FREE first): Groq → OpenAI → Anthropic
        if os.getenv("GROQ_API_KEY"):
            try:
                print("🟢 Using Groq LLM (FREE tier!)")
                from livekit.plugins.openai import LLM as OpenAICompatLLM
                original_openai_key = os.environ.get("OPENAI_API_KEY")
                original_base_url = os.environ.get("OPENAI_BASE_URL")
                os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")
                os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"
                try:
                    llm_instance = OpenAICompatLLM(model="llama-3.1-8b-instant")
                    print("✅ Groq LLM initialized successfully")
                finally:
                    if original_openai_key is not None:
                        os.environ["OPENAI_API_KEY"] = original_openai_key
                    else:
                        os.environ.pop("OPENAI_API_KEY", None)
                    if original_base_url is not None:
                        os.environ["OPENAI_BASE_URL"] = original_base_url
                    else:
                        os.environ.pop("OPENAI_BASE_URL", None)
            except Exception as e:
                print(f"⚠️ Groq LLM failed: {e}")

        if llm_instance is None and os.getenv("OPENAI_API_KEY"):
            try:
                print("🟧 Using OpenAI LLM (Deepgram STT/TTS + OpenAI LLM)")
                from livekit.plugins import openai as _openai
                llm_instance = _openai.LLM(model="gpt-4o-mini")
            except Exception as e:
                print(f"⚠️ OpenAI LLM failed: {e}")

        if llm_instance is None and os.getenv("ANTHROPIC_API_KEY"):
            try:
                print("🟦 Trying Anthropic Claude LLM...")
                from livekit.plugins.openai import LLM as OpenAICompatLLM
                llm_instance = OpenAICompatLLM(model="claude-3-5-haiku-latest")
                print("✅ Using Anthropic Claude LLM")
            except Exception as e:
                print(f"⚠️ Anthropic LLM failed: {e}")

        if llm_instance is None:
            raise RuntimeError(
                "\n❌ LLM required but not available!\n"
                "Deepgram provides STT/TTS but not LLM.\n\n"
                "🆓 FREE OPTION (recommended): Add GROQ_API_KEY from https://console.groq.com/\n"
                "Or add OPENAI_API_KEY / ANTHROPIC_API_KEY, or remove DEEPGRAM_API_KEY to use OpenAI for all."
            )
    else:
        # No Deepgram → require OpenAI for STT/TTS
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "\n❌ No voice provider configured.\n"
                "Set one of these in .env.local:\n"
                "  - DEEPGRAM_API_KEY (uses Deepgram STT/TTS + Groq/OpenAI/Claude for LLM)\n"
                "  - OPENAI_API_KEY (uses OpenAI STT/TTS/LLM)\n"
            )

        print("🟧 Using OpenAI STT/TTS/LLM (Deepgram not configured)")
        stt = openai.STT()
        tts = openai.TTS(voice="alloy")
        llm_instance = openai.LLM(model="gpt-4o-mini")
    
    # Create function tools using function_tool decorator
    from livekit.agents.llm import function_tool
    
    @function_tool(
        name="check_knowledge_base",
        description="Check if we have information about the caller's question in our knowledge base. Use this before answering questions about specific services, pricing, or treatments."
    )
    async def check_kb_tool(question: str) -> str:
        """Check knowledge base for question"""
        return check_knowledge_base(question)
    
    @function_tool(
        name="request_help",
        description="Request help from supervisor when you don't know the answer to a question. Call this when you cannot find information in the knowledge base."
    )
    async def request_help_tool(question: str) -> str:
        """Request help from supervisor"""
        return request_help(question)
    
    tools = [check_kb_tool, request_help_tool]
    
    # Create chat context with system message
    chat_ctx = llm.ChatContext()
    chat_ctx.add_message(
        role="system",
        content=SALON_PROMPT,
    )
    
    # Create agent with all components
    agent = Agent(
        instructions=SALON_PROMPT,
        chat_ctx=chat_ctx,
        tools=tools,
        vad=vad,
        stt=stt,
        llm=llm_instance,
        tts=tts,
    )
    
    # Create and start agent session
    session = AgentSession(
        vad=vad,
        stt=stt,
        llm=llm_instance,
        tts=tts,
    )
    await session.start(agent, room=ctx.room)
    
    print("✅ Agent started and ready to handle conversation")
    
    # Keep running until room disconnects
    while ctx.room.isconnected:
        await asyncio.sleep(1)


if __name__ == "__main__":
    # Run agent via LiveKit CLI
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
