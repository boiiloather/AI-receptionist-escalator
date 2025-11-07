# How to Generate LiveKit Room Token

If you need to generate a room token manually:

## Method 1: LiveKit Cloud Dashboard

1. Go to: https://cloud.livekit.io/
2. Login to your account
3. Click on project: **"AI receptionist escalation"**
4. Look for:
   - **"Developer Tools"** tab
   - OR **"Tokens"** section
   - OR **"Room Management"**
5. Click **"Generate Token"** or **"Create Token"**
6. Fill in:
   - **Room Name**: `test-room` (any name)
   - **Participant Name**: `user` (any name)
   - **Permissions**: Check "Can publish", "Can subscribe", "Can join"
7. Click **"Generate"** or **"Create"**
8. Copy the token (long string)
9. Paste in playground "room token..." field

## Method 2: Using LiveKit CLI (Advanced)

If you have LiveKit CLI installed:

```bash
livekit-cli token \
  --api-key APIvX9HSM4mmgxP \
  --api-secret nrZuZKRCl7YjjABNeVXBmnbS3fCiym4Uwc8lIJS7FYF \
  --join --room test-room --identity user
```

## Method 3: Use "LiveKit Cloud" Option (Easiest!)

The playground has a "LiveKit Cloud" option that does this automatically:
- Just select your project
- It generates the token for you
- No manual steps needed!






