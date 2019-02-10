"""
This file contains tests for the password reset feature
where the user who forgets their password can reset it
via a verification link sent directly into their registerd
mailbox.
"""
from .base_class import BaseTest
import json
from rest_framework import status
from .test_data.password_reset_data import (
    reset_link, invalid_reset_link,
    registered_email, unregistered_email, new_valid_password,
    new_blank_password, new_invalid_password, new_short_password
)
from django.urls import reverse


class ResetPassword(BaseTest):

    def setUp(self):
        super().setUp()
        self.register_test_user()
        self.password_reset_request_url = reverse(
            'authentication:request-password-reset'
        )

    def test_request_password_reset_registered_user(self):
        """test user with valid account requests password reset"""
        response = self.client.post(
            self.password_reset_request_url,
            data=json.dumps(
                registered_email
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_password_reset_unregistered_user(self):
        """test user with no account requests for a password reset"""
        response = self.client.post(
            self.password_reset_request_url,
            data=json.dumps(
                unregistered_email
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_password_reset_valid_link(self):
        """
        test user uses valid reset link sent to their email
        to access password reset endpoint
        """
        response = self.client.get(
            reset_link,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_password_reset_invalid_link(self):
        """test user uses invalid reset link to access password reset endpoint
        """
        response = self.client.get(
            invalid_reset_link,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_valid_password(self):
        """test user tries to reset to a valid password"""
        response = self.client.post(
            reset_link,
            data=json.dumps(
                new_valid_password
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_short_password(self):
        """test user tries to supply an undesirable short password"""
        response = self.client.post(
            reset_link,
            data=json.dumps(
                new_short_password
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_invalid_password(self):
        """test user tries to supply a password with forbidden characters"""
        response = self.client.post(
            reset_link,
            data=json.dumps(
                new_invalid_password
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_blank_password(self):
        """test user tries to supply an empty password"""
        response = self.client.post(
            reset_link,
            data=json.dumps(
                new_blank_password
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
