from rest_framework.reverse import reverse

from authors.apps.authentication.tests.base_class import BaseTest as AuthBaseT
from authors.apps.comments.models import Comment
from authors.apps.notifications.models import Notification
from .test_data import notification


class BaseTest(AuthBaseT):
    def setUp(self):
        super().setUp()

        self.notification_settings_url = reverse('notifications:settings')
        self.get_notifications_url = reverse('notifications:notifications')
        self.mark_notifications_as_read_url = reverse('notifications:read')

    @staticmethod
    def create_test_notification(user):
        test_notification = Notification(**notification)
        test_notification.save()
        test_notification.recipients.add(user.profile)
        return test_notification

    @staticmethod
    def create_test_comment(user, article):
        comment = Comment(body="Test comment", author=user.profile,
                          article=article)
        comment.save()
        return comment
