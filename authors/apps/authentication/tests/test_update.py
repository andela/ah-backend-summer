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
        self.url_login = reverse('authentication:login')

    def test_user_can_successfully_update_email(self):
        """Test that an existing user can successfully update their email"""
        user = self.activated_user()
        self.assertTrue(User.objects.get(email=valid_login_data['user']['email']))
        self.client.force_authenticate(user=user)
        response = self.client.patch(self.url_update, data=update_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(ObjectDoesNotExist, User.objects.get, email=valid_login_data['user']['email'])

    def test_user_can_retrieve_account_information(self):
        """Test that an existing user can retrieve their account info"""
        user = self.activated_user()
        self.assertTrue(User.objects.get(email=valid_login_data['user']['email']))
        
        resp = self.client.post(self.url_login, data=valid_login_data, format='json')
        token = resp.data['token']

        response = self.client.patch(self.url_update, 
                                    HTTP_AUTHORIZATION=f'Bearer {token}',
                                    data=update_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(ObjectDoesNotExist, User.objects.get, email=valid_login_data['user']['email'])
