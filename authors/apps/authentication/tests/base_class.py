"""Test base class file containing setup"""
import json

from rest_framework.test import APITestCase, APIClient

from django.urls import reverse


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.url_register = reverse('authentication:register')
