"""Test base class file containing setup"""
import json
from .test_data import valid_register_data_2

from rest_framework.test import APITestCase, APIClient

from django.urls import reverse


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.url_register = reverse('authentication:register')
        self.url_login = reverse('authentication:login')

    def register_user(self):
        self.client.post(self.url_register,
                         data=json.dumps(
                             valid_register_data_2),
                         content_type='application/json')
