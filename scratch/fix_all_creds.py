import re
import os

creds_dir = 'c:/Users/USER/OneDrive/Desktop/coding/orr_big/orr/google_credentials'
for filename in os.listdir(creds_dir):
    if filename.endswith('.json'):
        path = os.path.join(creds_dir, filename)
        with open(path, 'r') as f:
            content = f.read()
        
        # Replace \ followed by any char that's not n, r, t, f, b, u, ", /, \ with \n followed by that char
        new_content = re.sub(r'\\(?![nrtfbu"/\\])', r'\\n', content)
        
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"FIXED: {filename}")
        else:
            print(f"NO CHANGES: {filename}")
