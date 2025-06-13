from nacl.signing import SigningKey
from base64 import b64encode, b64decode
import json

# Your signing private key (base64 string)
signing_private_key_b64 = "QQ8CQupV64cMbC5+HabvzO6Pr+Ssh6YR9lrdLsukRMc="
signing_key = SigningKey(b64decode(signing_private_key_b64))

# Your subscribe payload (use the exact JSON you will POST)
payload = {
  "context": {
    "operation": {
      "ops_no": 1
    }
  },
  "message": {
    "request_id": "a2c0e81b-fdb1-4c94-8b0f-eef0babc29c4",
    "timestamp": "2025-06-13T19:29:21.971Z",
    "entity": {
      "gst": {
        "legal_entity_name": "Janmasoft Excelutions LLP",
        "business_address": "42 Moo Street, Cowtown, Bangalore, Karnataka 560001",
        "city_code": [
          "std:080"
        ],
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
      "callback_url": "/on_search",
      "key_pair": {
        "signing_public_key": "4JAK/9yauqLMOuh0J0GR2UfdnprwCzNcFtI8EgO6tJU=",
        "encryption_public_key": "MCowBQYDK2VuAyEARO4+4rbFiqHFJsewSS1wdaKjWWmXqMQJwPF7HgjLWWY=",
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
        "city_code": [
          "std:080"
        ]
      }
    ]
  }
}

# Convert payload to canonical JSON string (ensure no extra spaces)
payload_json_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

# Sign the payload
signed = signing_key.sign(payload_json_str.encode('utf-8'))

# Base64 encode the signature
signature_b64 = b64encode(signed.signature).decode('utf-8')

print("Signature for Authorization header:")
print(signature_b64)
