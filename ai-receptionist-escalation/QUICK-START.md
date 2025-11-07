# Quick Start Guide - Running the Agent

## Step 1: Open Command Prompt

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. OR open PowerShell

## Step 2: Navigate to Project Folder

```bash
cd C:\Users\Pravin\Downloads\ai-receptionist-escalation
```

## Step 3: Activate Virtual Environment

```bash
venv\Scripts\activate
```

You should see `(venv)` appear at the beginning of your command line.

## Step 4: Run the Agent

```bash
python run_agent.py dev
```

If you want to use Deepgram instead of OpenAI, add to `.env.local`:

```
DEEPGRAM_API_KEY=your-deepgram-api-key
```

The agent will automatically switch to Deepgram STT/TTS/LLM when this is set.

## Step 5: What You Should See

If everything works, you'll see:
```
🤖 Starting AI Receptionist Agent...
📁 Project root: C:\Users\Pravin\Downloads\ai-receptionist-escalation
🔥 Pre-warming agent services...
✅ Firebase initialized successfully
✅ Services initialized successfully
```

Then the agent will connect to LiveKit and wait for calls.

## Step 6: Test in Playground

1. Keep the agent terminal running (don't close it)
2. Go to https://agents-playground.livekit.io/
3. Enter your LiveKit URL: `wss://ai-receptionist-escalation-r2qait9g.livekit.cloud`
4. Click "Generate Token" or enter manually
5. Click "Connect"
6. You should see "Agent connected" turn green
7. Start chatting!

## Troubleshooting

### If you see "ModuleNotFoundError"
- Make sure virtual environment is activated (you see `(venv)`)
- Run: `pip install -r requirements.txt`

### If you see "Firebase error"
- The agent can still work, but help requests won't be saved
- Check that `firebase-service-account.json` exists in the project folder

### If agent doesn't connect
- Check your `.env.local` file has correct LiveKit credentials
- Make sure you're using the right LiveKit project URL


