import requests

url = "https://staging.registry.ondc.org/subscribe"
headers = {
  "Content-Type": "application/json"
}

payload = {
  "context": {
    "operation": {
      "ops_no": 1
    }
  },
  "message": {
    "request_id": "56faee8c-52c6-4bf3-a4df-40bd32930934",
    "timestamp": "2025-06-11T12:00:21.971Z",
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
        "signing_public_key": "65OofsUIgk+KrG1dHS0h/1rp7yC6cVE9v6TJRn8ZG9g=",
        "encryption_public_key": "MCowBQYDK2VuAyEA2WMWzMF06jHi4bIq/4mAgemhbTNK8lTU4tTt0ez2vUo=",
        "valid_from": "2025-06-12T12:00:00.291Z",
        "valid_until": "2026-06-12T12:00:00.290Z"}
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
