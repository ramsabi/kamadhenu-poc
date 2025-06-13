from nacl.public import PrivateKey
from base64 import b64decode, b64encode

private_key_b64 = "wK8zkn0OjR3GnE1l2Je4Jm1UgJK0nJNHjk4NPkAOwHI="
private_key = PrivateKey(b64decode(private_key_b64))
public_key = private_key.public_key

print("Derived Public Key:", b64encode(public_key.encode()).decode())
