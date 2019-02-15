from authors.apps.notifications.models import NotificationStatus, \
    NotificationSettings
from authors.apps.notifications.tasks import send_email


def send_notification_emails(notification):
    for recipient in notification.recipients.all():
        notification_status, _ = NotificationStatus.objects.get_or_create(
            recipient=recipient, notification=notification)

        notification_settings, _ = NotificationSettings.objects.get_or_create(
            profile=recipient)

        if not notification_status.email_was_sent and \
                notification_settings.allow_email_notifications:
            send_email.delay(subject=notification.title,
                             message=notification.body,
                             to=[recipient.user.email]).then(
                lambda: notification_status.set_email_status_as_sent())

    return True
