import os
import django
import json
from datetime import datetime, timedelta

import sys
# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from admin_portal.services import CalendarService
from admin_portal.models import Meeting

def test_google_meet():
    print("--- Testing Google Meet API Connection ---")
    
    # Check if we have a meeting to test with
    meeting = Meeting.objects.last()
    if not meeting:
        print("No meeting found in database to test with.")
        return

    print(f"Testing with Meeting ID: {meeting.id}")
    print(f"Current link: {meeting.meeting_link}")
    
    # Try to generate a link
    try:
        event_id = CalendarService.create_calendar_event(meeting)
        if event_id:
            meeting.refresh_from_db()
            print("SUCCESS!")
            print(f"New Real Link: {meeting.meeting_link}")
            print(f"Calendar Event ID: {meeting.calendar_event_id}")
        else:
            print("FAILED: create_calendar_event returned None. Check credentials or API permissions.")
    except Exception as e:
        print(f"CRASHED: {str(e)}")

if __name__ == "__main__":
    test_google_meet()
