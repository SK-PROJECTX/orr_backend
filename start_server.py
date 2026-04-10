#!/usr/bin/env python
"""
Script to start Django development server with correct settings
"""
import os
import sys
import subprocess

def main():
    # Set the correct Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    # Start the Django development server
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()