import requests

url = "http://127.0.0.1:8000/register"

data = {
    "username": "soham",
    "email": "soham@example.com",
    "password": "mypassword"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
