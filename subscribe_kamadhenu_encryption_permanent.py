import requests

url = "https://staging.registry.ondc.org/subscribe"

headers = {
    "Content-Type": "application/json",
    "Authorization": f'Signature keyId="kamadhenu-poc.onrender.com",algorithm="ed25519",signature="uQg0t9jf73rQOuxa/1+6pR9SwVauOqdfnUKE1WAyCderTipIPtbCQZJ28GFLktK3NHeBkpdhum5xZ7RcAGYhBQ=="'
}

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
      "callback_url": "/on_subscribe",
      "key_pair": {
        "signing_public_key": "y0BeTEWUIyE0uLamm1syQAhVQzCOf3UuSgAB60lxkvs=",
        "encryption_public_key": "MCowBQYDK2VuAyEAm8YhrgoYbiLwibQwwZj/phGP+Y8dxULSbB8nujPrTxs=",
        "valid_from": "2025-06-17T03:45:00.000Z",
        "valid_until": "2026-06-13T03:44:00.000Z"}
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

response = requests.post(url, headers=headers, json=payload, verify=False)
print("Status Code:", response.status_code)
print("Response:", response.text)
