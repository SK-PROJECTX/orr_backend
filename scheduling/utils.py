from .models import Event
from django.db.models import Q

def slot_conflicts(calendar_id, start_dt, duration_minutes=60, ignore_event_id=None):
    """
    Returns True if an event exists that overlaps with [start_dt, start_dt + duration]
    Default duration: 60 minutes (adjust from front-end if variable)
    """
    from django.utils import timezone
    end_dt = start_dt + timezone.timedelta(minutes=duration_minutes)
    qs = Event.objects.filter(calendar_id=calendar_id, cancelled=False)
    if ignore_event_id:
        qs = qs.exclude(pk=ignore_event_id)
    return qs.filter(start__lt=end_dt, end__gt=start_dt).exists()