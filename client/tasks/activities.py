from datetime import timezone

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


@shared_task
def invalidate_recommendations_cache(user_id: int):
    cache_key = f"dashboard_overview_{user_id}"
    cache.delete(cache_key)


@shared_task
def rebuild_recommendations_cache(user_id: int):
    from services.activities.recommendation import get_recommended_steps

    from ..models import Activity

    user = User.objects.get(id=user_id)
    recommendations = get_recommended_steps(user)
    recent_activities = Activity.objects.filter(user=user)[:10]

    data = {
        "recent_activities": [...],
        "recommendations": recommendations,
        "cached_at": timezone.now().isoformat(),
    }
    cache.set(f"dashboard_overview_{user_id}", data, timeout=60 * 30)
