from nacl.signing import SigningKey
from base64 import b64decode, b64encode
import json

# Signing key
signing_private_key_b64 = "scxpvbEecQKghnnhVgfBvq/o6cy7VwynSJJsUiZPvg3LQF5MRZQjITS4tqabWzJACFVDMI5/dS5KAAHrSXGS+w=="
signing_key = SigningKey(b64decode(signing_private_key_b64))

# Your clean payload
payload = {
  "context": {
    "operation": {
      "ops_no": 1
    }
  },
  "message": {
    "request_id": "a2c0e81b-fdb1-4c94-8b0f-eef0babc29c4",
    "timestamp": "2025-06-17T02:42:21.971Z",
    "entity": {
      "gst": {
        "legal_entity_name": "Janmasoft Excelutions LLP",
        "business_address": "42 Moo Street, Cowtown, Bangalore, Karnataka 560001",
        "city_code": ["std:080"],
        "gst_no": "29ABCDE1234F2Z5"
      },
      "pan": {
        "name_as_per_pan": "Sabitha Ramakrishnan",
        "pan_no": "GSPPS2229E",
        "date_of_incorporation": "13/09/1967"
      },
      "name_of_authorised_signatory": "Sabitha Ramakrishnan",
      "email_id": "ceo@janmasoft.com",
      "mobile_no": 7338811803,
      "country": "IND",
      "subscriber_id": "kamadhenu-poc.onrender.com",
      "unique_key_id": "a2c0e81b-fdb1-4c94-8b0f-eef0babc29c4",
      "callback_url": "/on_subscribe",
      "key_pair": {
        "signing_public_key": "y0BeTEWUIyE0uLamm1syQAhVQzCOf3UuSgAB60lxkvs=",
        "encryption_public_key": "MCowBQYDK2VuAyEAm8YhrgoYbiLwibQwwZj/phGP+Y8dxULSbB8nujPrTxs=",
        "valid_from": "2025-06-13T09:45:00.000Z",
        "valid_until": "2026-06-13T09:45:00.000Z"
      }
    },
    "network_participant": [
      {
        "subscriber_url": "/bapl",
        "domain": "ONDC:TRV10",
        "type": "buyerApp",
        "msn": False,
        "city_code": ["std:080"]
      }
    ]
  }
}

# Canonical JSON
payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

# Sign
signed = signing_key.sign(payload_str.encode('utf-8'))
signature_b64 = b64encode(signed.signature).decode('utf-8')

print("Signature for Authorization header:")
print(signature_b64)

