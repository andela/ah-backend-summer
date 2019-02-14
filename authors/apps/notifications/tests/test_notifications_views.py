from rest_framework import status

from authors.apps.notifications.models import NotificationSettings
from authors.apps.notifications.tests import test_data
from authors.apps.notifications.tests.base import BaseTest


class NotificationViewsTests(BaseTest):
    def test_user_can_retrieve_their_notification_settings(self):
        user = self.activated_user()
        self.client.force_authenticate(user)
        response = self.client.get(self.notification_settings_url,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['allow_email_notifications'], True)

    def test_user_can_update_notification_settings(self):
        user = self.activated_user()
        self.client.force_authenticate(user)
        notification_settings = NotificationSettings.objects.create(
            profile=user.profile)
        self.assertTrue(notification_settings.allow_email_notifications)
        response = self.client.patch(self.notification_settings_url,
                                     format='json',
                                     data=test_data.email_notifications_off)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification_settings = NotificationSettings.objects.get(
            profile=user.profile)
        self.assertFalse(notification_settings.allow_email_notifications)
