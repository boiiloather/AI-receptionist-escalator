# Setup Instructions

Complete guide to setting up and running the AI Receptionist Escalation System.

## Prerequisites

1. **Python 3.8+** installed
2. **LiveKit account** (free tier) - https://livekit.io/
3. **Firebase Realtime Database** (free tier) - https://firebase.google.com/
4. **Groq API key** (free LLM) - https://console.groq.com/
5. **Deepgram API key** (free STT/TTS) - https://console.deepgram.com/ (optional but recommended)

## Step 1: Clone and Install Dependencies

```bash
# Navigate to project directory
cd ai-receptionist-escalation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure Firebase

1. **Create Firebase Project**
   - Go to https://console.firebase.google.com/
   - Create a new project
   - Enable Realtime Database (not Firestore)
   - Set security rules (for development):
     ```json
     {
       "rules": {
         ".read": true,
         ".write": true
       }
     }
     ```

2. **Download Service Account Key**
   - Go to Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file as `firebase-service-account.json` in the project root

3. **Get Database URL**
   - Go to Realtime Database in Firebase Console
   - Copy the database URL (e.g., `https://your-project.firebaseio.com`)

## Step 3: Configure LiveKit

1. **Create LiveKit Account**
   - Sign up at https://livekit.io/
   - Create a new project
   - Get your API keys from the dashboard:
     - URL (e.g., `wss://your-project.livekit.cloud`)
     - API Key
     - API Secret

2. **Get Access Token** (for testing)
   - Use LiveKit's token generator or CLI to create tokens
   - Or use their playground for testing

## Step 4: Configure Environment Variables

Create a `.env.local` file in the project root:

```bash
# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase-service-account.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com

# LLM Configuration (choose ONE - FREE options available!)
# Option 1: Groq (FREE, fast, recommended!)
GROQ_API_KEY=your-groq-api-key
# Get free key at: https://console.groq.com/
# Free tier: 6000 tokens/minute

# Option 2: OpenAI (paid)
OPENAI_API_KEY=your-openai-api-key

# Option 3: Anthropic Claude (paid)
ANTHROPIC_API_KEY=your-anthropic-api-key

# Deepgram Configuration (recommended - FREE STT/TTS)
DEEPGRAM_API_KEY=your-deepgram-api-key
# Get free key at: https://console.deepgram.com/
# Free tier: 12,000 minutes/month

# Default Caller Phone (for testing)
DEFAULT_CALLER_PHONE=+1234567890

# Request Timeout (hours)
REQUEST_TIMEOUT_HOURS=4
```

## Step 5: Run the System

### Terminal 1: Start the AI Agent

```bash
# Make sure virtual environment is activated
python run_agent.py dev
```

You should see:
```
🤖 Starting AI Receptionist Agent...
📁 Project root: /path/to/project
🔥 Pre-warming agent services...
✅ Services initialized successfully
```

### Terminal 2: Start the Supervisor UI

```bash
# Make sure virtual environment is activated
python run_supervisor.py
```

You should see:
```
🌐 Starting Supervisor Web UI...
📁 Project root: /path/to/project
🔗 Visit: http://localhost:5000
✅ Background timeout checker started
 * Running on http://127.0.0.1:5000
```

## Step 6: Test the System

### Test Flow:

1. **Connect to Agent** (using LiveKit playground)
   - Visit https://agents-playground.livekit.io/
   - Select "LiveKit Cloud" → Choose your project
   - OR use "Manual" → Enter URL: `wss://your-project.livekit.cloud` + token
   - Wait for "Agent connected" to turn green

2. **Test Unknown Question**
   - Ask: "Do you offer keratin treatments?"
   - Agent checks KB → not found → creates help request
   - Agent responds: "Let me check with my supervisor and get back to you on that."
   - Check agent console for help request creation

3. **Check Supervisor UI**
   - Visit http://localhost:5000/pending
   - You should see the pending request with the question

4. **Submit Answer**
   - Enter answer: "Yes, we offer keratin treatments for $150. It takes approximately 3 hours."
   - Click "✅ Respond"
   - Check console for simulated text to customer
   - Request moves to "Resolved"

5. **Verify Knowledge Base Update**
   - Visit http://localhost:5000/knowledge-base
   - You should see the new Q&A entry

6. **Test Repeat Question**
   - Ask the same question again: "Do you offer keratin treatments?"
   - Agent checks KB → finds answer → responds immediately!
   - No escalation needed

## Troubleshooting

### Firebase Connection Issues

- **Error: "Firebase credentials file not found"**
  - Ensure `firebase-service-account.json` is in project root
  - Check `FIREBASE_CREDENTIALS_PATH` in `.env.local`

- **Error: "Permission denied"**
  - Check Firebase security rules
  - Ensure database is Realtime Database (not Firestore)

### LiveKit Connection Issues

- **Error: "Connection failed"**
  - Verify `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` in `.env.local`
  - Check network connectivity
  - Ensure LiveKit project is active

### Agent Not Responding

- **Agent doesn't trigger help requests**
  - Check console logs for errors
  - Verify OpenAI API key is set
  - Check that KB and help services initialized successfully

### Supervisor UI Not Loading

- **Port 5000 already in use**
  - Change port in `run_supervisor.py`: `app.run(debug=True, port=5001)`
  
- **Firebase errors in UI**
  - Check browser console for errors
  - Verify Firebase credentials are correct

## Architecture Notes

- **Agent**: LiveKit voice agent handles calls and escalates unknown questions
- **Help Request Service**: Creates requests and notifies supervisor
- **Firebase**: Stores help requests and knowledge base
- **Supervisor UI**: Flask web app for managing requests
- **Background Jobs**: Auto-timeout checker runs every hour

## Next Steps

- Add authentication to supervisor UI
- Integrate real SMS via Twilio
- Improve KB search with embeddings
- Add analytics and reporting
- Deploy to production



