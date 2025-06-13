from nacl.public import PrivateKey, PublicKey, Box
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives import serialization

# Your DER base64 public key
der_b64 = "MCowBQYDK2VuAyEARO4+4rbFiqHFJsewSS1wdaKjWWmXqMQJwPF7HgjLWWY="
der_bytes = b64decode(der_b64)

# Extract raw public key from DER
pub_key = serialization.load_der_public_key(der_bytes)
raw_pub_key_bytes = pub_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

# Form PublicKey object
encryption_pub_key = PublicKey(raw_pub_key_bytes)

# Generate ephemeral sender key
sender_private_key = PrivateKey.generate()
sender_public_key = sender_private_key.public_key

# Encrypt message
box = Box(sender_private_key, encryption_pub_key)
plaintext = b"Hello, Kamadhenu!"
encrypted = box.encrypt(plaintext)

# Prepare payload
import json
payload = {
    "message": {
        "sender_public_key": b64encode(sender_public_key.encode()).decode(),
        "encrypted_payload": b64encode(encrypted).decode()
    }
}
print(json.dumps(payload, indent=2))
