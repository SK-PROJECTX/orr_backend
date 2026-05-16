import json

try:
    with open('c:/Users/USER/OneDrive/Desktop/coding/orr_big/orr/google_credentials/google-docs-credentials.json', 'r') as f:
        data = json.load(f)
    print("JSON is valid")
except Exception as e:
    print(f"Error: {e}")
