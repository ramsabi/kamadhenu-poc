from nacl.public import PrivateKey, PublicKey, Box
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import serialization

# Your public encryption key (DER base64 from ONDC subscribe payload)
encryption_pub_key_b64 = "MCowBQYDK2VuAyEARO4+4rbFiqHFJsewSS1wdaKjWWmXqMQJwPF7HgjLWWY="

# Load your public key
der_bytes = b64decode(encryption_pub_key_b64)
pub_key = serialization.load_der_public_key(der_bytes)
raw_pub_key_bytes = pub_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)
your_pub_key = PublicKey(raw_pub_key_bytes)

# Generate ephemeral ONDC private key (simulating ONDC encryption step)
ondc_private_key = PrivateKey.generate()

# Create box and encrypt
box = Box(ondc_private_key, your_pub_key)
plaintext = b"Hello Kamadhenu"
encrypted = box.encrypt(plaintext)

# Output base64 challenge
challenge_b64 = b64encode(encrypted).decode('utf-8')
print("Challenge for testing /on_subscribe:")
print(challenge_b64)
