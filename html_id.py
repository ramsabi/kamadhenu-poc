from nacl.signing import SigningKey
from base64 import b64decode, b64encode

REQUEST_ID = "a2c0e81b-fdb1-4c94-8b0f-eef0babc29c4"
SIGNING_PRIVATE_KEY_B64 = "scxpvbEecQKghnnhVgfBvq/o6cy7VwynSJJsUiZPvg3LQF5MRZQjITS4tqabWzJACFVDMI5/dS5KAAHrSXGS+w=="

# Decode and take first 32 bytes (seed)
private_key_bytes = b64decode(SIGNING_PRIVATE_KEY_B64)
seed = private_key_bytes[:32]

signing_key = SigningKey(seed)

# Sign
signed = signing_key.sign(REQUEST_ID.encode('utf-8'))
SIGNED_UNIQUE_REQ_ID = b64encode(signed.signature).decode('utf-8')

print("SIGNED_UNIQUE_REQ_ID:")
print(SIGNED_UNIQUE_REQ_ID)

