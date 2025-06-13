from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from base64 import b64decode
import os
import uvicorn

from nacl.public import PrivateKey, PublicKey, Box
from nacl.exceptions import CryptoError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

app = FastAPI()

# Base64 DER-encoded ONDC encryption private key (from cryptic_utils.py)
ENCRYPTION_PRIVATE_KEY_B64 = "MC4CAQAwBQYDK2VuBCIEIMhKv07BXNkjg/TpZwBC/CDDjHP9LwwQTbw04NV06g5Q"

# Decode DER to 32-byte raw private key
encryption_der_bytes = b64decode(ENCRYPTION_PRIVATE_KEY_B64)
private_key_obj = serialization.load_der_private_key(
    encryption_der_bytes,
    password=None,
    backend=default_backend()
)
raw_private_key_bytes = private_key_obj.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)
private_key = PrivateKey(raw_private_key_bytes)

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
