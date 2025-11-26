from typing import List, Dict
from client.models import Activity

def get_recommended_steps(user) -> List[Dict]:
    """Business rules engine for next steps"""
    recommendations = []

    if not user.meeting_requests.exists():
        recommendations.append({
            "title": "Request your first meeting",
            "message": "Schedule your initial consultation to begin.",
            "action_type": "Meeting Activity",
            "priority": 1
        })

   

    return sorted(recommendations, key=lambda x: x["priority"])