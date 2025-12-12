#!/usr/bin/env python
import requests
import json
import uuid

def test_client_focused():
    print("Testing client creation endpoint (focused)...")
    
    # Login first
    login_url = "http://127.0.0.1:8000/api/auth/login/"
    login_data = {
        "username": "testadmin",
        "password": "testpass123"
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            data = login_result.get('data', {})
            access_token = data.get('accessToken')
            
            if access_token:
                print("Login successful")
                
                # Test client creation
                client_url = "http://127.0.0.1:8000/admin-portal/v1/clients/"
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                
                unique_id = str(uuid.uuid4())[:8]
                client_data = {
                    "username": f"apiclient_{unique_id}",
                    "email": f"apiclient_{unique_id}@example.com",
                    "full_name": f"API Client {unique_id}",
                    "company": "API Test Company",
                    "role": "Manager",
                    "stage": "discover",
                    "primary_pillar": "strategic"
                }
                
                print(f"Creating client with data: {client_data}")
                client_response = requests.post(client_url, json=client_data, headers=headers)
                print(f"Client creation status: {client_response.status_code}")
                
                if client_response.status_code == 201:
                    print("[SUCCESS] Client created successfully!")
                    try:
                        response_data = client_response.json()
                        print(f"Created client: {response_data}")
                    except:
                        print("Response is not JSON")
                elif client_response.status_code == 400:
                    print("[ERROR] Bad request - validation error")
                    try:
                        error_data = client_response.json()
                        print(f"Validation errors: {error_data}")
                    except:
                        print(f"Error response: {client_response.text[:500]}")
                elif client_response.status_code == 500:
                    print("[ERROR] Internal server error")
                    # Try to extract just the error message
                    response_text = client_response.text
                    if "Exception Value:" in response_text:
                        # Extract the exception from Django debug page
                        start = response_text.find("Exception Value:")
                        if start != -1:
                            end = response_text.find("</td>", start)
                            if end != -1:
                                error_msg = response_text[start:end]
                                print(f"Exception: {error_msg}")
                    else:
                        print("No exception details found in response")
                else:
                    print(f"[ERROR] Unexpected status: {client_response.status_code}")
                    print(f"Response: {client_response.text[:200]}")
            else:
                print("No access token received")
        else:
            print(f"Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"Test error: {e}")

if __name__ == '__main__':
    test_client_focused()