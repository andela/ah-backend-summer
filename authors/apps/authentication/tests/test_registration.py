"""Tests for user registration"""
import json
from rest_framework import status
from .test_data.register_data import (valid_register_data, register_short_password,
                                      register_no_email, register_no_password,
                                      register_no_username, register_invalid_email,
                                      register_no_username_password_email)
from .base_class import BaseTest


class RegistrationTest(BaseTest):

    def test_user_register_successful(self):
        """Test user registration passes with correct user data"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(
                                        valid_register_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"],
                         valid_register_data["user"]["email"])
        self.assertEqual(response.data["username"],
                         valid_register_data["user"]["username"])

    def test_user_register_password_short(self):
        """Test user registration fails with short password"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(
                                        register_short_password),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["password"])

    def test_user_register_no_email(self):
        """Test user registration fails when no email is provided"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(register_no_email),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["email"])

    def test_user_register_no_password(self):
        """Test user registration fails when no password is provided"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(register_no_password),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["password"])

    def test_user_register_no_username(self):
        """Test user registration fails when no username is provided"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(register_no_username),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["username"])

    def test_user_register_no_username_email_password(self):
        """Test user registration fails when no username, email and password are provided"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(
                                        register_no_username_password_email),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["username"])
        self.assertIsNotNone(response.data["errors"]["password"])
        self.assertIsNotNone(response.data["errors"]["email"])

    def test_user_register_invalid_email(self):
        """Test user registration fails with invalid email structure"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(register_invalid_email),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["email"])
