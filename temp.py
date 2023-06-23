import requests
import json

url = "http://localhost:13311"

payload = json.dumps({
  "region": 1,
  "wealth": 1,
  "age": 1,
  "education": 2,
  "age_of_first": 17,
  "working_status": 1,
  "marital": 2,
  "internet": 1,
  "alcohol": 5,
  "ethnicity": 1,
  "sex": 0
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)