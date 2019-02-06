import json
import os

from django.test import TestCase
from django.urls import reverse

from ..models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.username = 'buffalo'
        self.email = 'buffalo@mail.com'
        self.password = 'krs1krs1'

    def test_user_creation(self):
        response = User.objects.create_user(username=self.username,
                                            email=self.email,
                                            password=self.password)
        self.assertEqual(response.get_full_name, 'buffalo')

    def test_super_user_creation(self):
        response = User.objects.create_superuser(username=self.username,
                                                 email=self.email,
                                                 password=self.password)
        self.assertEqual(response.get_full_name, 'buffalo')

    def test_super_user_missing_password(self):
        with self.assertRaises(TypeError):
            response = User.objects.create_superuser(username=self.username,
                                                     email=self.email,
                                                     password=None)

    def test_missing_email(self):
        with self.assertRaises(TypeError):
            response = User.objects.create_user(username=self.username,
                                                email=None,
                                                password=self.password)

    def test_missing_username(self):
        with self.assertRaises(TypeError):
            response = User.objects.create_user(username=None,
                                                email=self.email,
                                                password=self.password)

    def test_str_return_method(self):
        response = User.objects.create_user(username=self.username,
                                            email=self.email,
                                            password=self.password)
        self.assertEqual(str(response), 'buffalo@mail.com')

    def test_return_short_name(self):
        response = User.objects.create_user(username=self.username,
                                            email=self.email,
                                            password=self.password)
        self.assertEqual(response.get_short_name, 'buffalo')
