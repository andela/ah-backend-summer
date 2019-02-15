from celery import shared_task
from django.core.mail import get_connection, EmailMultiAlternatives, send_mail
from django.conf import settings


@shared_task
def send_email(subject, message, to, from_email=settings.DEFAULT_FROM_EMAIL,
               html_message=None):
    send_mail(subject, message, from_email, to, html_message=html_message)
