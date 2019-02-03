"""Test base class file containing setup"""
import json

from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data.login_data import valid_login_data
from .test_data.register_data import valid_register_data

from rest_framework.test import APITestCase, APIClient

from django.urls import reverse


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.url_register = reverse('authentication:register')
        self.url_login = reverse('authentication:login')
        self.url_user_detail = reverse('authentication:retrieve_update')

    def register_test_user(self):
        self.client.post(self.url_register,
                         data=json.dumps(
                             valid_register_data),
                         content_type='application/json')

    def register_and_login_test_user(self):
        self.register_test_user()
        # force authentication for now, since the login system is not implemented yet
        test_user = User.objects.get(email=valid_login_data['user']['email'])
        self.client.force_authenticate(user=test_user)
        # we'll use this when the token based auth system is ready
        # self.client.credentials(HTTPS_AUTHORIZATION="Bearer {}".format(
        #     self.client.post(self.url_login, data=valid_login_data, format='json').data["token"]))
