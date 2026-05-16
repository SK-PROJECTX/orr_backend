import json
import os

creds_dir = 'c:/Users/USER/OneDrive/Desktop/coding/orr_big/orr/google_credentials'
for filename in os.listdir(creds_dir):
    if filename.endswith('.json'):
        path = os.path.join(creds_dir, filename)
        try:
            with open(path, 'r') as f:
                json.load(f)
            print(f"{filename}: VALID")
        except Exception as e:
            print(f"{filename}: INVALID - {e}")
