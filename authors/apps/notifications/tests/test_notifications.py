from unittest.mock import MagicMock, patch

from django.core import mail

from authors.apps.notifications.signals import Notification
from authors.apps.notifications.models import NotificationSettings, \
    NotificationStatus
from authors.apps.notifications.tasks import send_email
from authors.apps.notifications.tests.base import BaseTest
from authors.apps.notifications.utils.notification_utils import \
    send_notification_emails
from . import test_data


class UtilTests(BaseTest):
    def test_send_notification_emails_properly_calls_send_email(self):
        send_email_delay_mock = MagicMock()
        send_email.delay = send_email_delay_mock

        notification = self.create_test_notification(self.activated_user())

        self.assertTrue(send_notification_emails(notification))
        self.assertEqual(send_email_delay_mock.call_count,
                         notification.recipients.count())

    def test_send_notification_emails_sends_to_only_those_who_opt_in(self):
        user = self.activated_user()
        notification_settings, _ = NotificationSettings.objects.get_or_create(
            profile=user.profile)
        notification_settings.toggle_email_notifications(False)
        notification = self.create_test_notification(user)
        send_email_delay_mock = MagicMock()
        send_email.delay = send_email_delay_mock

        self.assertTrue(send_notification_emails(notification))
        send_email_delay_mock.assert_not_called()

    def test_send_notification_emails_sends_only_unsent_emails(self):
        user = self.activated_user()
        notification = self.create_test_notification(user)
        notification_status, _ = NotificationStatus.objects.get_or_create(
            recipient=user.profile, notification=notification)
        notification_status.set_email_status_as_sent()
        send_email_delay_mock = MagicMock()
        send_email.delay = send_email_delay_mock

        self.assertTrue(send_notification_emails(notification))
        send_email_delay_mock.assert_not_called()


class TaskTests(BaseTest):
    def test_send_email(self):
        self.assertEqual(len(mail.outbox), 0)
        send_email(test_data.email['subject'], test_data.email['message'],
                   to=[self.activated_user()])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, test_data.email['subject'])


class ModelTests(BaseTest):
    def test_notification_settings_are_both_true_by_default(self):
        user = self.activated_user()
        notification_settings, created = \
            NotificationSettings.objects.get_or_create(profile=user.profile)
        self.assertTrue(notification_settings.allow_email_notifications)
        self.assertTrue(notification_settings.allow_in_app_notifications)


class SignalTests(BaseTest):
    def test_on_follow_action_notify_followed_party_receives_signal(self):
        user = self.activated_user()
        user2 = self.create_another_user_in_db()
        queue_notification_emails = "authors.apps.notifications.signals." \
                                    "Notification.queue_notification_emails"
        with patch(
                queue_notification_emails) as queue_notification_emails_mock:
            queue_notification_emails_mock.assert_not_called()
            user.profile.follow(user2.profile)
            queue_notification_emails_mock.assert_called_once()
