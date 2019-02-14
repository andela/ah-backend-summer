from rest_framework import status
from rest_framework.utils import json

from authors.apps.notifications.models import Notification
from authors.apps.notifications.tests.base import BaseTest


class TestNotifications(BaseTest):
    def test_get_unread_in_app_notifications_returns_the_right_number(self):
        user = self.activated_user()
        self.assertEqual(
            len(Notification.get_unread_in_app_notifications(user.profile)), 0)
        article = self.create_article(user)
        user2 = self.create_another_user_in_db()
        self.create_test_comment(user2, article)
        self.assertEqual(
            len(Notification.get_unread_in_app_notifications(user.profile)), 1)

    def test_unread_in_app_notifications_view_returns_the_right_number(self):
        user = self.activated_user()
        self.client.force_authenticate(user)
        response = self.client.get(self.get_notifications_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data['notifications'])), 0)
        article = self.create_article(user)
        user2 = self.create_another_user_in_db()
        self.create_test_comment(user2, article)
        response = self.client.get(self.get_notifications_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data['notifications'])), 1)

    def test_mark_notifications_as_unread(self):
        user = self.activated_user()
        self.client.force_authenticate(user)
        article = self.create_article(user)
        user2 = self.create_another_user_in_db()
        self.create_test_comment(user2, article)
        response = self.client.get(self.get_notifications_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data['notifications'])), 1)
        response = self.client.post(self.mark_notifications_as_read_url,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Marked all as read")
        response = self.client.get(self.get_notifications_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data['notifications'])), 0)
