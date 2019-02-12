from ..authentication.models import UserManager, User
from rest_framework import serializers
import jwt
import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail


class PasswordResetManager:
    """
    This class handles the operations involved in the email-based
    password-reset feature including preparing the email message,
    reset link and verification of link and updating password
    """

    def __init__(self, request):
        self.sender_email = "teamabasama@gmail.com"
        self.subject = "You requested a password reset"
        self.password_reset_url = request.build_absolute_uri(
            '/api/v1/user/reset-password/')

    def get_user_by_email(self, email):
        email = UserManager.normalize_email(email)
        try:
            user = User.objects.get(email=email)
            return user
        except Exception:
            return None

    def prepare_password_reset_email(self, email):
        user = self.get_user_by_email(email)

        if user is None:
            raise serializers.ValidationError(
                "There is no user with this email address!")

        # parameters for password reset email to be sent
        self.requester_email = user.email
        self.encoded_token = jwt.encode({
            "email": self.requester_email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        self.context = {
            'username': user.username,
            'reset_link': self.password_reset_url +
            self.encoded_token.decode('utf-8') + '/'
        }
        self.email_body = render_to_string(
            'password_reset_email.txt', self.context)

        return self.email_body

    def send_password_reset_email(self, email):
        self.prepare_password_reset_email(email)
        send_mail(
            self.subject,
            self.email_body,
            self.sender_email,
            [self.requester_email],
            fail_silently=False
        )
        return self.encoded_token.decode('utf-8')

    def update_password(self, email, new_password):
        user = self.get_user_by_email(email)
        user.set_password(new_password)
        user.save()

    def get_user_from_encoded_token(self, token):
        try:
            payload_data = jwt.decode(
                token, settings.SECRET_KEY, algorithm='HS256')
            return payload_data
        except Exception:
            return None
