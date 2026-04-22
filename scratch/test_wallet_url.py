import requests

BASE_URL = "http://localhost:8000"
# Since we need authentication, I'll check if I can hit it without or if I need a token.
# For now, let's just see if it returns 401 or 404. 401 means the path is FOUND.
try:
    response = requests.get(f"{BASE_URL}/wallet/balance/")
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")
