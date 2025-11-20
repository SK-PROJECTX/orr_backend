from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

token_generator = PasswordResetTokenGenerator()


def build_verify_password_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    base = settings.FRONTEND_VERIFY_EMAIL_URL
    return f"{base}?uid={uid}&token={token}&email={user.email}"

def create_password_reset_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    base = settings.FRONTEND_RESET_PASSWORD_URL
    return f"{base}?uid={uid}&token={token}"

    