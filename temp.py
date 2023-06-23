import requests
import json

url = "http://localhost:13311"

payload = json.dumps({
  "region": 1,
  "wealth": 1,
  "age": 9,
  "education": 0,
  "age_of_first": 8,
  "working_status": 0,
  "marital": 2,
  "internet": 0,
  "alcohol": 30,
  "ethnicity": 1,
  "sex": 0
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)