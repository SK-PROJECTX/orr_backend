with open('c:/Users/USER/OneDrive/Desktop/coding/orr_big/orr/google_credentials/google-calendar-credentials.json', 'r') as f:
    lines = f.readlines()
    line5 = lines[4]
    snippet = line5[960:980]
    print(f"Snippet: '{snippet}'")
