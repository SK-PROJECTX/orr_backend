import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_google_docs():
    creds_path = 'c:/Users/USER/OneDrive/Desktop/coding/orr_big/orr/google_credentials/google-docs-credentials.json'
    scopes = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
    
    print(f"--- Testing Google Docs API with {creds_path} ---")
    
    try:
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
        service = build('docs', 'v1', credentials=creds)
        
        print("Attempting to create a test document...")
        doc = service.documents().create(body={'title': 'Antigravity Test Doc'}).execute()
        print(f"SUCCESS! Created document with ID: {doc.get('documentId')}")
        
    except Exception as e:
        print(f"FAILED: {e}")
        if "permission" in str(e).lower():
            print("\nDIAGNOSIS: This is definitely a permission issue.")
            print("1. Check if the Service Account 'google-docs@orr-core-platform.iam.gserviceaccount.com' is DISABLED in IAM.")
            print("2. Check if there are any Organization Policies blocking the Docs API.")
        else:
            print(f"\nDIAGNOSIS: Unexpected error type: {type(e)}")

if __name__ == "__main__":
    test_google_docs()
