"""
AI Receptionist Agent Launcher
Handles Python path and starts the LiveKit agent
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run
from agent.ai_agent import entrypoint, prewarm
from livekit import agents

if __name__ == "__main__":
    print("🤖 Starting AI Receptionist Agent...")
    print(f"📁 Project root: {project_root}")
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
