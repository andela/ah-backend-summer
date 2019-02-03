from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status

from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base_class import BaseTest
from authors.apps.authentication.tests.test_data.login_data import valid_login_data
from authors.apps.authentication.tests.test_data.update_data import update_email


class UpdateTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.url_update = reverse('authentication:retrieve_update')

    def test_user_can_successfully_update_email(self):
        """Test that an existing user can successfully update their email"""
        self.register_and_login_test_user()
        self.assertTrue(User.objects.get(email=valid_login_data['user']['email']))
        response = self.client.patch(self.url_update, data=update_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(ObjectDoesNotExist, User.objects.get, email=valid_login_data['user']['email'])
