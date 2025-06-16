from flask import Flask, request, jsonify, Response
from nacl.public import PrivateKey, PublicKey, Box
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives import serialization
import os

app = Flask(__name__)

# Key values provided by user
REQUEST_ID = "a2c0e81b-fdb1-4c94-8b0f-eef0babc29c4"
SIGNING_PRIVATE_KEY = "QQ8CQupV64cMbC5+HabvzO6Pr+Ssh6YR9lrdLsukRMc="
SIGNING_PUBLIC_KEY = "4JAK/9yauqLMOuh0J0GR2UfdnprwCzNcFtI8EgO6tJU="
ENCRYPTION_PRIVATE_KEY = "oBzWRu/6+W2HPQ5Sm8TWeKpY7HpASgym7z/X90LPBro="
ENCRYPTION_PUBLIC_KEY = "MCowBQYDK2VuAyEARO4+4rbFiqHFJsewSS1wdaKjWWmXqMQJwPF7HgjLWWY="
ONDC_PUBLIC_KEY = "MCowBQYDK2VuAyEAduMuZgmtpjdCuxv+Nc49K0cB6tL/Dj3HZetvVN7ZekM="

@app.route("/on_subscribe", methods=["POST"])
def on_subscribe():
    data = request.get_json()
    encrypted_challenge = b64decode(data.get("challenge"))
    
    # Load ONDC public key
    ondc_pub_der = b64decode(ONDC_PUBLIC_KEY)
    ondc_pub_key = serialization.load_der_public_key(ondc_pub_der)
    ondc_pub_raw = ondc_pub_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    ondc_pub = PublicKey(ondc_pub_raw)
    
    # Load our encryption private key
    priv_raw = b64decode(ENCRYPTION_PRIVATE_KEY)
    priv = PrivateKey(priv_raw)
    
    # Decrypt challenge
    box = Box(priv, ondc_pub)
    try:
        decrypted = box.decrypt(encrypted_challenge)
        return Response(decrypted, mimetype='text/plain')
    except Exception as e:
        return Response(f"Decryption failed: {str(e)}", status=400, mimetype='text/plain')



@app.route("/ondc-site-verification.html", methods=["GET"])
def site_verification():
    html_content = f'<html><head><meta name="ondc-site-verification" content="{REQUEST_ID}"/></head><body>ONDC Site Verification</body></html>'
    return Response(html_content, mimetype='text/html')
    

@app.route("/")
def index():
    return "Kamadhenu service placeholder"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5556))
    app.run(host="0.0.0.0", port=port)
