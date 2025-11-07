"""
Quick script to generate a LiveKit room token for testing
"""
from livekit import api
import os
from dotenv import load_dotenv

# Load environment
load_dotenv('.env.local')

# Get credentials
url = os.getenv('LIVEKIT_URL')
api_key = os.getenv('LIVEKIT_API_KEY')
api_secret = os.getenv('LIVEKIT_API_SECRET')

if not all([url, api_key, api_secret]):
    print("❌ Error: Missing LiveKit credentials in .env.local")
    print("   Required: LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET")
    exit(1)

# Create access token
token = api.AccessToken(api_key, api_secret) \
    .with_identity("playground-user") \
    .with_name("Playground User") \
    .with_grants(api.VideoGrants(
        room_join=True,
        can_publish=True,
        can_subscribe=True,
    ))

print("\n" + "="*60)
print("🔑 LiveKit Token Generated")
print("="*60)
print(f"\n📡 URL:")
print(f"   {url}")
print(f"\n🔐 Token:")
print(f"   {token.to_jwt()}")
print("\n" + "="*60)
print("\n💡 Instructions:")
print("   1. Copy the URL above")
print("   2. Copy the Token above")
print("   3. In playground, click 'Manual'")
print("   4. Paste URL and Token")
print("   5. Click 'Connect'")
print("="*60 + "\n")

