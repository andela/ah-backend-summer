"""Tests for user registration"""
import json
from django.core import mail
from django.urls import reverse
from rest_framework import status
from .test_data.register_data import (
    valid_register_data, register_short_password,
    register_no_email, register_no_password,
    register_no_username, register_invalid_email,
    register_no_username_password_email, register_invalid_password,
    expired_link, invalid_link)
from .test_data import login_data
from .base_class import BaseTest


class RegistrationTest(BaseTest):
    """
    unit tests for all modules under user registration
    """

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

    def test_activation_email_is_sent_on_valid_registration(self):
        """
        Test activation email is sent to user email upon
        succesful registration.
        """
        self.register_test_user()
        self.assertEqual(
            "Activation for your Author's Haven account",
            mail.outbox[0].subject)
        self.assertIn(
            "Thank you, Please Activate your account below.",
            mail.outbox[0].body)

    def test_successful_account_activation(self):
        """
        Test when a user clicks on emailed activation link,
        account is successfully acitvated.
        """
        response = self.register_and_activate_test_user()
        self.assertEqual(
            response.data['msg'],
            "Your account is activated, enjoy")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_activate_an_already_activated_account(self):
        """
        Test user can not activate an already activated account.
        """
        self.register_test_user()
        token = (mail.outbox[0].body.split("\n").pop(1).split(
            'email-verification/')[1])
        url = reverse('authentication:activate', args=[token])
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reactivate = self.client.get(url, content_type='application/json')
        self.assertEqual(
            reactivate.data['msg'], "This account is already activated")
        self.assertEqual(reactivate.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_activate_a_nonexistant_account(self):
        """
        Test user can not activate an account that doesnot exist.
        """
        valid_token = login_data.valid_token_unexisting_user
        url = reverse('authentication:activate', args=[valid_token])
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(
            response.data['err_msg'],
            "User matching query does not exist.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_password_short(self):
        """Test user registration fails with short password"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(
                                        register_short_password),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data["errors"]["password"])

    def test_user_register_password_invalid_characters(self):
        """Test user registration fails with invalid characters in password"""
        response = self.client.post(self.url_register,
                                    data=json.dumps(
                                        register_invalid_password),
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
        """
        Test user registration fails when no username,
        email and password are provided
        """
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

    """
    Integration tests for all modules under user registration
    """

    def test_cannot_activate_with_expired_link(self):
        """
        Test user can not access activateion view with an expired token.
        """
        url = expired_link
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(
            response.data['err_msg'], "Token expired")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_activate_with_invalid_link(self):
        """
        Test user can not access activation view with an invalid token.
        """
        url = invalid_link
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(
            response.data['err_msg'], "Invalid token")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
