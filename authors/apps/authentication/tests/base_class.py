"""Test base class file containing setup"""
import json
from .test_data.register_data import valid_register_data

from rest_framework.test import APITestCase, APIClient

from django.urls import reverse


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.url_register = reverse('authentication:register')
        self.url_login = reverse('authentication:login')

    def register_test_user(self):
        self.client.post(self.url_register,
                         data=json.dumps(
                             valid_register_data),
                         content_type='application/json')
