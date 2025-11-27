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
    latest_request = user.meeting_requests.order_by("-created_at").first()

    if latest_request:
        if not (latest_request.basic_context and latest_request.goals and latest_request.pain_points):
            recommendations.append({
                "title": "Complete pre-meeting checklist",
                "message": "Help your consultant understand your needs before the meeting.",
                "action_type": "Meeting Preparation",
                "priority": 2,
                "meeting_request_id": latest_request.id
            })

   

    return sorted(recommendations, key=lambda x: x["priority"])