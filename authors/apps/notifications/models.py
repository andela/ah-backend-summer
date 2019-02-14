from django.db import models

from django.db.models import CASCADE, PROTECT

from authors.apps.profiles.models import Profile


class Notification(models.Model):
    """
    Notification object. This was intentionally kept small an contains only
    the information specific to a notification
    """
    title = models.CharField(max_length=200)
    body = models.TextField()
    recipients = models.ManyToManyField(to=Profile,
                                        related_name='notifications',
                                        related_query_name='notification')

    def queue_notification_emails(self):
        from authors.apps.notifications.utils import notification_utils
        notification_utils.send_notification_emails(self)

    @staticmethod
    def get_unread_in_app_notifications(profile):
        """
        :param profile: user profile whose notifications we're interested in
        :return: the user's unread in-app notifications
        """
        all_notifications = Notification.objects.filter(recipients=profile)
        unread_notifications = []
        for notification in all_notifications:
            notification_status, _ = NotificationStatus.objects.get_or_create(
                recipient=profile, notification=notification)
            if not notification_status.was_read_in_app:
                unread_notifications.append(notification)
        return unread_notifications

    def __str__(self):
        return "Title: {}, To: {}".format(self.title, self.recipients.all())

    @staticmethod
    def mark_all_unread_as_read(profile):
        """
        mark all notifications as read in-app
        :param profile: the user whose notifications we shall be targeting
        """
        for notification in Notification.get_unread_in_app_notifications(
                profile):
            notification_status = NotificationStatus.objects.get(
                recipient=profile, notification=notification)
            notification_status.set_in_app_notification_as_read()


class NotificationStatus(models.Model):
    """
    Status of a given notification.
    This is specific to a user for every notification
    A better way to do this would be with some kind of hash map, but there is
    no model field that does this in a clean way, hence this approach
    """
    recipient = models.ForeignKey(to=Profile, on_delete=CASCADE)
    notification = models.ForeignKey(to=Notification, on_delete=PROTECT)
    was_read_in_app = models.BooleanField(default=False)
    email_was_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('recipient', 'notification')

    def set_in_app_notification_as_read(self):
        self.was_read_in_app = True
        self.save()

    def set_email_status_as_sent(self):
        self.email_was_sent = True
        self.save()


class NotificationSettings(models.Model):
    """
    The notification settings for a particular user
    """
    profile = models.OneToOneField(to=Profile, on_delete=CASCADE)
    allow_in_app_notifications = models.BooleanField(default=True)
    allow_email_notifications = models.BooleanField(default=True)

    def toggle_email_notifications(self, status):
        self.allow_email_notifications = status
        self.save()
