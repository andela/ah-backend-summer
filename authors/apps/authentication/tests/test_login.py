"""Tests for user login"""
import json
from django.core import mail
from rest_framework import status
from .test_data.login_data import (valid_login_data, login_no_email,
                                   login_no_password, login_unregistered_email,
                                   login_invalid_email, login_invalid_password,
                                   login_no_email_password)
from .base_class import BaseTest


class LoginTest(BaseTest):

    def test_login_successful(self):
        """Test user login passes with correct user credentials"""
        self.register_and_activate_test_user()
        response = self.client.post(self.url_login,
                                    data=json.dumps(
                                        valid_login_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"],
                         valid_login_data["user"]["email"])

    def test_login_no_email(self):
        """Test user login fails when no email is provided"""

        response = self.client.post(self.url_login,
                                    data=json.dumps(login_no_email),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["email"])

    def test_login_no_password(self):
        """Test user login fails when no password is provided"""

        response = self.client.post(self.url_login,
                                    data=json.dumps(
                                        login_no_password),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["password"])

    def test_login_user_unregistered(self):
        """Test user login fails when user is not registered"""

        response = self.client.post(self.url_login,
                                    data=json.dumps(
                                        login_unregistered_email),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_email(self):
        """Test user login fails with invalid email structure"""

        response = self.client.post(self.url_login,
                                    data=json.dumps(
                                        login_invalid_email),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_password(self):
        """Test user login fails when password provided is short"""

        response = self.client.post(self.url_login,
                                    data=json.dumps(
                                        login_invalid_password),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_no_email_password(self):
        """Test user login fails when no email and password are provided"""

        response = self.client.post(self.url_login,
                                    data=json.dumps(
                                        login_no_email_password),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["email"])
        self.assertIsNotNone(response.data["errors"]["password"])
