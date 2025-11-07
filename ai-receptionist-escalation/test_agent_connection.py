"""
Quick test script to verify agent configuration and connection
"""
import os
from dotenv import load_dotenv

print("🔍 Checking Agent Configuration...")
print("=" * 60)

# Load environment
load_dotenv('.env.local')

# Check LiveKit config
livekit_url = os.getenv('LIVEKIT_URL')
livekit_key = os.getenv('LIVEKIT_API_KEY')
livekit_secret = os.getenv('LIVEKIT_API_SECRET')

print("\n📡 LiveKit Configuration:")
print(f"  URL: {livekit_url}")
print(f"  API Key: {livekit_key[:10]}...{'✅' if livekit_key else '❌ NOT FOUND'}")
print(f"  API Secret: {'✅ SET' if livekit_secret else '❌ NOT FOUND'}")

# Check OpenAI
openai_key = os.getenv('OPENAI_API_KEY')
print(f"\n🤖 OpenAI Configuration:")
print(f"  API Key: {'✅ SET' if openai_key else '❌ NOT FOUND'}")

# Check Firebase
firebase_url = os.getenv('FIREBASE_DATABASE_URL')
firebase_creds = os.getenv('FIREBASE_CREDENTIALS_PATH')
print(f"\n🔥 Firebase Configuration:")
print(f"  Database URL: {firebase_url}")
print(f"  Credentials Path: {firebase_creds}")

# Check if credentials file exists
if firebase_creds:
    import os.path
    if not os.path.isabs(firebase_creds):
        firebase_creds = os.path.join(os.getcwd(), firebase_creds.replace('./', ''))
    exists = os.path.exists(firebase_creds)
    print(f"  Credentials File: {'✅ EXISTS' if exists else '❌ NOT FOUND'}")

print("\n" + "=" * 60)
print("✅ Configuration check complete!")
print("\n💡 Next steps:")
print("  1. Make sure virtual environment is activated")
print("  2. Run: python run_agent.py dev")
print("  3. Wait for agent to connect to LiveKit")
print("  4. Then try the playground again")






