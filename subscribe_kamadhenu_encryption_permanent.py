import requests

url = "https://staging.registry.ondc.org/subscribe"

signature = "ijfa1r1frxXS+vjav5itYbK+x2NBLUAkT0DceRM0eMqpGH/HNU1kXvQq/+9s0bZNYoeeU5YC6fVdrY3L6wv7BQ=="

headers = {
    "Content-Type": "application/json",
    "Authorization": f'Signature keyId="kamadhenu-poc.onrender.com",algorithm="ed25519",signature="{signature}"'
}

payload = {
  "context": {
    "operation": {
      "ops_no": 1
    }
  },
  "message": {
    "request_id": "56faee8c-52c6-4bf3-a4df-40bd32930934",
    "timestamp": "2025-06-13T13:21:21.971Z",
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
      "unique_key_id": "56faee8c-52c6-4bf3-a4df-40bd32930934",
      "callback_url": "/on_search",
      "key_pair": {
        "signing_public_key": "pX1QQ4zRxq0iRJDlGoTNSKdgCare4zYjoumavbUNpNY=",
        "encryption_public_key": "MCowBQYDK2VuAyEABmH6BGD4c3zgjZZMU81FhU1XpA7BKfEQx3H5ISMtiGs=",
        "valid_from": "2025-06-12T09:45:00.000Z",
        "valid_until": "2026-06-12T09:45:00.000Z"}
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
