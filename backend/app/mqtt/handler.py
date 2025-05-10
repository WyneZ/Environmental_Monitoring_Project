from services.auth import decode_token
import json

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    token = payload.get("token")

    if not token:
        print("❌ No token provided")
        return

    decoded = decode_token(token)
    if not decoded:
        print("❌ Invalid token")
        return

    device_id = decoded["sub"]
    print(f"✅ Authenticated device: {device_id}")
    # Save sensor data, etc.
