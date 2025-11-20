from client.utils import create_password_reset_url
from notification.utils import notify_user


def send_password_reset_notification(user):
    """
    Send a password reset email to the user with UID + token URL.
    """

    reset_url = create_password_reset_url(user)

    notify_user(
        user,
        "Reset Your Password",
        "Click the link below to reset your password.",
        ["email"],
        {
            "template": "accounts/password_reset_email.html",
            "context": {
                "name": user.first_name or user.username,
                "reset_url": reset_url,
            },
        },
    )
