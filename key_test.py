from cryptography.hazmat.primitives import serialization
from base64 import b64decode

# Your Base64 private key (replace this with your actual key)
ENCRYPTION_PRIVATE_KEY_B64 = "RpwfrbCloRBJfDZ6ZePJ7QS2EiHe9kENa40OgiLKJF5eWqH0VsZpq1XMXq4UcToADF6gseOyBJ2vTycdrWeFzQ=="

# Decode the Base64 key
private_key_bytes = b64decode(ENCRYPTION_PRIVATE_KEY_B64)

# Try to load it as a DER-encoded private key
try:
    private_key = serialization.load_der_private_key(
        private_key_bytes,
        password=None,
        backend=None
    )
    print("Private key loaded successfully")
except Exception as e:
    print(f"Error loading private key: {e}")
