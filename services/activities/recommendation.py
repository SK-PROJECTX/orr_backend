from typing import Dict, List
from admin_portal.models import Meeting


def get_recommended_steps(user) -> List[Dict]:
    """Business rules engine for next steps"""
    recommendations = []

    onboarding = getattr(user, "onboarding", None)
    if not onboarding or not onboarding.is_completed:
        recommendations.append(
            {
                "title": "Complete your onboarding",
                "message": "Finish your profile and preferences so we can personalise your experience.",
                "action_type": "Onboarding",
                "priority": 1,
            })

    latest_meeting = Meeting.objects.filter(client__user=user).order_by("-created_at").first()

    if not latest_meeting:
        recommendations.append(
            {
                "title": "Request your first meeting",
                "message": "Schedule your initial consultation to get started.",
                "action_type": "Meeting",
                "priority": 1,
            }
        )
        return recommendations  
    missing_fields = []

    if not getattr(latest_meeting, "agenda", None):
        missing_fields.append("agenda")


    if missing_fields and latest_meeting.status in ["requested", "confirmed"]:
        recommendations.append(
            {
                "title": "Complete your meeting preparation",
                "message": "Provide more details so the consultant can prepare effectively.",
                "action_type": "Meeting Preparation",
                "priority": 2,
                "meeting_id": latest_meeting.id,
            }
        )

    if latest_meeting.status == "completed" and not latest_meeting.meeting_notes:
        recommendations.append(
            {
                "title": "Review your meeting summary",
                "message": "Add or review your notes to keep track of progress.",
                "action_type": "Post-Meeting",
                "priority": 3,
                "meeting_id": latest_meeting.id,
            }
        )


    return sorted(recommendations, key=lambda x: x["priority"])
