with open('c:/Users/USER/OneDrive/Desktop/coding/orr_big/orr/google_credentials/google-docs-credentials.json', 'r') as f:
    lines = f.readlines()
    line5 = lines[4] # 0-indexed
    print(f"Line 5 length: {len(line5)}")
    char_at_1102 = line5[1101] # 0-indexed
    snippet = line5[1090:1120]
    print(f"Snippet around 1102: '{snippet}'")
    print(f"Char at 1102: '{char_at_1102}'")
