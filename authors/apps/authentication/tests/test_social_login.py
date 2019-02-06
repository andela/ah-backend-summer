import json
from rest_framework import status
from unittest.mock import patch
from .base_class import BaseTest
from .test_data.social_auth_data import (
    invalid_twitter_secret, valid_twitter_token, invalid_twitter_token,
    invalid_twitter_token_missing_secret_and_token, valid_google_token,
    invalid_google_token, valid_facebook_token, invalid_facebook_token)


class TwitterAuthTest(BaseTest):
    """Tests for twitter user login authentication"""
    # patch() decorator / context manager makes it easy to mock classes or objects
    # in a module under test. The object you specify will be replaced with a mock
    # (or other object) during the test and restored when the test ends
    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_invalid_secret_user_is_new(self, TwitterCredentials):
        """Test twitter login fails with missing secret key for new user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        invalid_twitter_secret),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_invalid_token_user_is_new(self, TwitterCredentials):
        """Test twitter login fails with missing token key for new user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        invalid_twitter_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_invalid_secret_user_not_new(self, TwitterCredentials):
        """Test twitter login fails with missing secret key for new user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_twitter,
                         data=json.dumps(
                             invalid_twitter_secret),
                         content_type='application/json')
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        invalid_twitter_secret),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_invalid_token_user_not_new(self, TwitterCredentials):
        """Test twitter login fails with missing secret key for new user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_twitter,
                         data=json.dumps(
                             invalid_twitter_token),
                         content_type='application/json')
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        invalid_twitter_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_invalid_missing_token_secret_user_is_new(self, TwitterCredentials):
        """Test twitter login fails with missing token and secret key for new user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        invalid_twitter_token_missing_secret_and_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_invalid_missing_token_secret_user_not_new(self, TwitterCredentials):
        """Test twitter login fails with missing token and secret key for returning user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_twitter,
                         data=json.dumps(
                             invalid_twitter_token_missing_secret_and_token),
                         content_type='application/json')
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        invalid_twitter_token_missing_secret_and_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_user_is_new(self, TwitterCredentials):
        """Test twitter login passes with valid token for a new user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        valid_twitter_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('twitter.Api.VerifyCredentials')
    def test_twitter_login_user_not_new(self, TwitterCredentials):
        """Test twitter login passes with valid token for a returning user"""
        TwitterCredentials.return_value.__dict__ = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_twitter,
                         data=json.dumps(
                             valid_twitter_token),
                         content_type='application/json')
        response = self.client.post(self.url_twitter,
                                    data=json.dumps(
                                        valid_twitter_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GoogleAuthTest(BaseTest):
    """Tests for google user login authentication"""

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_login_new_user_successful(self, verify_google_oauth2_token):
        """Test google login passes with valid token for a new user"""
        verify_google_oauth2_token.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_google,
                                    data=json.dumps(
                                        valid_google_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_login_successful_user_not_new(self, verify_google_oauth2_token):
        """Test google login passes with valid token for a returning user"""
        verify_google_oauth2_token.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_google,
                         data=json.dumps(
                             valid_google_token),
                         content_type='application/json')
        response = self.client.post(self.url_google,
                                    data=json.dumps(
                                        valid_google_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_login_invalid_token_user_not_new(self, verify_google_oauth2_token):
        """Test google login fails with invalid token for a returning user"""
        verify_google_oauth2_token.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_google,
                         data=json.dumps(
                             invalid_google_token),
                         content_type='application/json')
        response = self.client.post(self.url_google,
                                    data=json.dumps(
                                        invalid_google_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_login_invalid_token_new_user(self, verify_google_oauth2_token):
        """Test google login fails with invalid token for a new user"""
        verify_google_oauth2_token.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_google,
                                    data=json.dumps(
                                        invalid_google_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FacebookAuthTest(BaseTest):
    """Tests for facebook user login authentication"""
    @patch('facebook.GraphAPI.get_object')
    def test_facebook_login_new_user_successful(self, user_object):
        """Test facebook login passes with valid token for a new user"""
        user_object.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_facebook,
                                    data=json.dumps(
                                        valid_facebook_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('facebook.GraphAPI.get_object')
    def test_facebook_login_not_new_user_successful(self, user_object):
        """Test facebook login passes with valid token for a returning user"""
        user_object.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_facebook,
                         data=json.dumps(
                             valid_facebook_token),
                         content_type='application/json')
        response = self.client.post(self.url_facebook,
                                    data=json.dumps(
                                        valid_facebook_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('facebook.GraphAPI.get_object')
    def test_facebook_login_new_user_invalid_token(self, user_object):
        """Test facebook login fails with invalid token for a new user"""
        user_object.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        response = self.client.post(self.url_facebook,
                                    data=json.dumps(
                                        invalid_facebook_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('facebook.GraphAPI.get_object')
    def test_facebook_login_not_new_user(self, user_object):
        """Test facebook login fails with invalid token for a returning user"""
        user_object.return_value = {
            'email': 'jon@mail.com',
            'name': 'Jon'
        }
        self.client.post(self.url_facebook,
                         data=json.dumps(
                             valid_facebook_token),
                         content_type='application/json')
        response = self.client.post(self.url_facebook,
                                    data=json.dumps(
                                        invalid_facebook_token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
