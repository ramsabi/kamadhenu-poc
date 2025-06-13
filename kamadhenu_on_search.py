from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from base64 import b64decode
import os
import uvicorn

from nacl.public import PrivateKey, PublicKey, Box
from nacl.exceptions import CryptoError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

app = FastAPI()

# Constants for decryption and signing
ENCRYPTION_PRIVATE_KEY = "oBzWRu/6+W2HPQ5Sm8TWeKpY7HpASgym7z/X90LPBro="  # Kamadhenu's private encryption key (base64 encoded)
ONDC_PUBLIC_KEY = "MCowBQYDK2VuAyEAduMuZgmtpjdCuxv+Nc49K0cB6tL/Dj3HZetvVN7ZekM="  # ONDC's public key (staging)
REQUEST_ID = "56faee8c-52c6-4bf3-a4df-40bd32930934"  # Unique request ID for tracking
SIGNING_PRIVATE_KEY = "RpwfrbCloRBJfDZ6ZePJ7QS2EiHe9kENa40OgiLKJF5eWqH0VsZpq1XMXq4UcToADF6gseOyBJ2vTycdrWeFzQ=="  # Kamadhenu's signing key for request_id signing

# Decode the base64 private key (which is currently base64 encoded)
private_key_bytes = b64decode(ENCRYPTION_PRIVATE_KEY)

# If the key is longer than 32 bytes, trim it to 32 bytes (NaCl requirement)
if len(private_key_bytes) > 32:
    private_key_bytes = private_key_bytes[:32]

# Check if the private key is now 32 bytes long
if len(private_key_bytes) != 32:
    raise ValueError(f"Private key must be 32 bytes long, but got {len(private_key_bytes)} bytes")

# Create the PrivateKey object using the 32-byte raw key
private_key = PrivateKey(private_key_bytes)


@app.post("/on_search")
async def on_search(request: Request):
    body = await request.json()
    print("Received on_search callback:")
    print(body)
    return {"message": "Kamadhenu received the rice list 🐄🍚"}

@app.post("/on_search/on_subscribe")
async def on_subscribe(request: Request):
    try:
        body = await request.json()
        print("🔔 Raw ONDC callback body:")
        print(body)

        # Step 1: Handle ONDC challenge verification
        if "challenge" in body:
            challenge = body["challenge"]
            print(f"⚡ Responding to ONDC challenge: {challenge}")
            return {"challenge": challenge}

        # Step 2: Handle encrypted callback
        message = body.get("message", {})
        print("🔍 Extracted 'message' block:")
        print(message)

        sender_pub_key_b64 = message.get("sender_public_key")
        encrypted_payload_b64 = message.get("encrypted_payload")

        if not sender_pub_key_b64 or not encrypted_payload_b64:
            print("⚠️ Missing 'sender_public_key' or 'encrypted_payload'")
            return JSONResponse(content={"error": "Missing required fields"}, status_code=200)

        sender_pub_key_bytes = b64decode(sender_pub_key_b64)
        sender_pub_key = PublicKey(sender_pub_key_bytes)

        # Decrypt the payload using Kamadhenu's private key and sender's public key
        box = Box(private_key, sender_pub_key)
        decrypted = box.decrypt(b64decode(encrypted_payload_b64)).decode('utf-8')

        print("✅ Decrypted ONDC payload:")
        print(decrypted)

        return {"status": "success", "message": decrypted}

    except CryptoError:
        print("❌ Decryption failed — CryptoError")
        return JSONResponse(content={"error": "Decryption failed"}, status_code=403)

    except Exception as e:
        print(f"💥 Internal error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/ondc-site-verification.html")
async def serve_verification_file():
    return FileResponse("ondc-site-verification.html", media_type='text/html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("kamadhenu_on_search:app", host="0.0.0.0", port=port)
