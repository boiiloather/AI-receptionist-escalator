# AI Receptionist Escalation System

> Transform AI agents from "fail or hallucinate" to "escalate and learn"

## 🎯 Overview

Production-grade escalation system for LiveKit AI agents. When the agent encounters unknown questions, it creates help requests for supervisors, learns from their answers, and becomes smarter over time.

## ✨ Features

- ✅ **LiveKit AI Agent** - Voice-enabled receptionist with salon business context
- ✅ **Intelligent Knowledge Base** - Fuzzy matching for paraphrased questions
- ✅ **Help Request System** - Automatic escalation with Firebase storage
- ✅ **Supervisor Web UI** - Dashboard for managing pending requests
- ✅ **Auto-Learning** - KB updates automatically when supervisor answers
- ✅ **Request Lifecycle** - Pending → Resolved/Unresolved with timeout handling
- ✅ **Free Tier Support** - Deepgram (STT/TTS) + Groq (LLM) - no paid services required
- ✅ **Modular Architecture** - Clean separation of concerns, production-ready

## 🏗️ Architecture

```
Call → Agent → KB Check → Known? → Answer
                     ↓ Unknown
              Help Request → DB → Notify Supervisor
                                        ↓
                              Supervisor UI → Answer
                                        ↓
                                  Update KB + Text Customer
```

## 🚀 Quick Start

See **SETUP-INSTRUCTIONS.md** for detailed setup guide.

### Prerequisites

- Python 3.8+
- LiveKit account (free tier)
- Firebase Realtime Database (free tier)
- Groq API key (free tier) - https://console.groq.com/
- Deepgram API key (free tier) - https://console.deepgram.com/

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
# Copy .env.example to .env.local and add your API keys:
#   - GROQ_API_KEY (free LLM)
#   - DEEPGRAM_API_KEY (free STT/TTS)
#   - LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
#   - FIREBASE_DATABASE_URL, FIREBASE_CREDENTIALS_PATH
```

### Running

```bash
# Terminal 1: Start the agent
python run_agent.py dev

# Terminal 2: Start supervisor UI (optional)
python run_supervisor.py
# Then visit http://localhost:5000
```

### Windows Quick Start

Double-click:
- `start_agent.bat` - Start agent
- `start_supervisor.bat` - Start supervisor UI

## 📖 Documentation

- **SETUP-INSTRUCTIONS.md** - Complete setup guide with troubleshooting
- **QUICK-START.md** - Step-by-step running instructions
- **CONNECT-TO-PLAYGROUND.md** - How to connect to LiveKit playground
- **tests/test_scenarios.py** - Test cases and scenarios

## 🧪 Quick Test

1. Start agent: `python run_agent.py dev`
2. Connect via LiveKit playground: https://agents-playground.livekit.io/
3. Ask: "Do you offer keratin treatments?"
4. Agent checks KB → if not found, creates help request
5. Visit http://localhost:5000/pending
6. Submit answer: "Yes, we offer keratin treatments..."
7. Ask again → agent answers from KB!

## ⚠️ Rate Limits

**Groq Free Tier**: 6,000 tokens per minute
- If you see rate limit errors, wait 30-60 seconds between questions
- The agent automatically retries with exponential backoff
- For production, consider upgrading to Groq Dev Tier or using OpenAI

**Deepgram Free Tier**: Generous limits for STT/TTS
- Should not hit limits during normal testing

## 🔧 Tech Stack

- **Agent Framework**: LiveKit Agents (Python SDK) v1.2.17
- **Voice Recognition**: Deepgram STT (Nova-2 model) - Free tier
- **Text-to-Speech**: Deepgram TTS (Aura voices) - Free tier
- **Language Model**: Groq (Llama 3.1 8B Instant) - Free tier, OpenAI-compatible
- **Database**: Firebase Realtime Database (free tier)
- **Web UI**: Flask 3.0+ with responsive templates
- **VAD**: Silero Voice Activity Detection
- **Error Handling**: Graceful degradation, retry logic, timeout management

## 📄 License

MIT License
