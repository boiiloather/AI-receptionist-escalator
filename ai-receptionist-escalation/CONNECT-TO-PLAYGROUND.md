# How to Connect to LiveKit Playground

## Option 1: Using LiveKit Cloud (Easiest)

1. **Make sure agent is running** (see below)
2. Go to: https://agents-playground.livekit.io/
3. Click **"LiveKit Cloud"** tab
4. Select **"AI receptionist escalation"** from the dropdown
5. Click **"Connect to playground"** or **"Connect"**
6. Wait 5-10 seconds for agent to connect
7. You should see "Agent connected" turn green/blue
8. Start chatting in the CHAT panel!

## Option 2: Manual Connection

1. **Make sure agent is running** (see below)
2. Go to: https://agents-playground.livekit.io/
3. Click **"Manual"** tab
4. Enter your URL:
   ```
   wss://ai-receptionist-escalation-r2qait9g.livekit.cloud
   ```
5. **Get a Room Token**:
   - Go to your LiveKit Cloud dashboard
   - Click on your project "AI receptionist escalation"
   - Go to "Room Tokens" or "Developer Tools"
   - Generate a token with:
     - Room name: any name (e.g., "test-room")
     - Participant name: "user"
     - Permissions: Join room
   - Copy the token
6. Paste the token in the playground "room token..." field
7. Click **"Connect"**
8. Wait 5-10 seconds for agent to connect
9. Start chatting!

## IMPORTANT: Agent Must Be Running First!

Before connecting to playground, you MUST have the agent running:

### Windows:
1. Double-click `start_agent.bat`
   OR
2. Open Command Prompt:
   ```bash
   cd C:\Users\Pravin\Downloads\ai-receptionist-escalation
   venv\Scripts\activate
   python run_agent.py dev
   ```

### What You Should See:
```
🤖 Starting AI Receptionist Agent...
📁 Project root: C:\Users\Pravin\Downloads\ai-receptionist-escalation
🔥 Pre-warming agent services...
✅ Services initialized successfully
```

**Keep this terminal window open!** The agent must stay running.

## Troubleshooting

### "Agent connected" stays gray/not connected:
- Make sure agent is running in terminal
- Wait 10-15 seconds for connection
- Check agent terminal for errors
- Try refreshing the playground page

### Can't generate token:
- Make sure you're logged into LiveKit Cloud
- Check you have access to the project
- Try the "LiveKit Cloud" option instead (easier!)

### Still not working:
- Check `.env.local` has correct LiveKit credentials
- Verify LIVEKIT_URL matches your project
- Make sure agent terminal shows no errors
