from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from nacl.public import PrivateKey, PublicKey, Box
from nacl.exceptions import CryptoError
from base64 import b64decode
import os
import uvicorn

app = FastAPI()

# ✅ Key material
ENCRYPTION_PRIVATE_KEY = "oBzWRu/6+W2HPQ5Sm8TWeKpY7HpASgym7z/X90LPBro="  # NP's encryption private key
ONDC_PUBLIC_KEY = "MCowBQYDK2VuAyEAduMuZgmtpjdCuxv+Nc49K0cB6tL/Dj3HZetvVN7ZekM="  # Registry's encryption public key
REQUEST_ID = "a2c0e81b-fdb1-4c94-8b0f-eef0babc29c4"  # Request ID sent in /subscribe
SIGNING_PRIVATE_KEY = "QQ8CQupV64cMbC5+HabvzO6Pr+Ssh6YR9lrdLsukRMc="  # NP's signing private key

# Prepare the PrivateKey object directly — no DER, no slicing
private_key = PrivateKey(b64decode(ENCRYPTION_PRIVATE_KEY))

@app.post("/on_search/on_subscribe")
async def on_subscribe(request: Request):
    try:
        body = await request.json()
        print("🔔 Received callback body:")
        print(body)

        if "challenge" in body:
            return {"challenge": body["challenge"]}

        message = body.get("message", {})
        sender_pub_key_b64 = message.get("sender_public_key")
        encrypted_payload_b64 = message.get("encrypted_payload")

        if not sender_pub_key_b64 or not encrypted_payload_b64:
            return JSONResponse(content={"error": "Missing required fields"}, status_code=200)

        sender_pub_key = PublicKey(b64decode(sender_pub_key_b64))
        box = Box(private_key, sender_pub_key)
        decrypted = box.decrypt(b64decode(encrypted_payload_b64)).decode('utf-8')
        print("✅ Decrypted payload:")
        print(decrypted)

        return {"status": "success", "message": decrypted}

    except CryptoError:
        print("❌ Decryption failed")
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

