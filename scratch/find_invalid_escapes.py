import re

with open('c:/Users/USER/OneDrive/Desktop/coding/orr_big/orr/google_credentials/google-docs-credentials.json', 'r') as f:
    content = f.read()

# Find backslashes NOT followed by n, r, t, f, b, u, ", /, or \
invalid_escapes = re.findall(r'\\(?![nrtfbu"/\\])', content)
print(f"Invalid escapes found: {invalid_escapes}")

# Find positions
for match in re.finditer(r'\\(?![nrtfbu"/\\])', content):
    print(f"Position: {match.start()}, Context: '{content[match.start()-10:match.start()+10]}'")
