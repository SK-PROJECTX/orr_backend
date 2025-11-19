from client.utils import build_verify_password_url
from notification.utils import notify_user


def send_email_verification_notification(user):
    """
    Send verification email to a newly registered user.
    """
    verification_url = build_verify_password_url(user)

    notify_user(
        user,
        "Verify Your Email Address",
        "Please verify your email to activate your account.",
        ["email"],
        {
            "template": "accounts/email_verification.html",
            "context": {
                "name": user.username or user.email,
                "verification_url": verification_url,
            },
        },
    )
