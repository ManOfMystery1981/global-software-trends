python -c "
import requests
url = 'http://localhost:3000/api/verify-and-fulfill'
payload = {'data': {'customer': {'email': 'test@example.com'}}}
response = requests.post(url, json=payload)
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')
"
