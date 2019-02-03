import json
import os

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .base_class import BaseTest
from .test_data import login_data, register_data


class TestUserJwtAuthentication (BaseTest):
    """This class tests The JWT authentcation
    it contains tests that test whether
    1. The token is returned on user registration and login
    2. Tests whether endpoints raise informative error messages ones
       a user misses out on providing the a Bearer token.
    """

    def test_user_login(self):
        self.client.post(self.url_register, data=json.dumps(
            register_data.valid_register_data), 
            content_type='application/json')
        response = self.client.post(reverse('authentication:login'), 
        data=json.dumps(
            login_data.valid_login_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_registration(self):
        response = self.client.post(self.url_register, data=json.dumps(
            register_data.valid_register_data), 
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_missing_token_and_bearer_prefix(self):
        response = self.client.post(self.url_user_detail,
            HTTP_AUTHORIZATION="")
        expected_dict = {
            "detail": "Authentication credentials were not provided."
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)

    def test_provide_long_bearer_token(self):
        response = self.client.post(self.url_user_detail,
            HTTP_AUTHORIZATION="Bearer jlasdngklasdgnklas token")
        expected_dict = {
            "detail": "sorry you have provided a long token"
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)

    def test_provide_wrong_bearer_prefix(self):
        response = self.client.post(self.url_user_detail,
            HTTP_AUTHORIZATION="Bearerrr jlasdngklasdgnklassdgsdgf")
        expected_dict = {
            "detail": "wrong prefix, please use Bearer"
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)

    def test_missing_bearer_prefix(self):
        response = self.client.get(self.url_user_detail,
            HTTP_AUTHORIZATION='j,asndg/lkbdsagdshmngj,asndg/lkbdsagdshmng')
        expected_dict = {
            "detail": "You should provide both the Bearer prefix and the token"
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)

    def test_missing_token(self):
        response = self.client.get(self.url_user_detail, 
            HTTP_AUTHORIZATION='Bearer ')
        expected_dict = {
            "detail": "You should provide both the Bearer prefix and the token"
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)
    
    def test_expired_token(self):
        response = self.client.get(self.url_user_detail, 
            HTTP_AUTHORIZATION='Bearer '+ login_data.expired_token)
        expected_dict = {
            "detail": "Token has expired."
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)

    def test_valid_token_with_non_existing_user(self):
        response = self.client.get(self.url_user_detail, 
            HTTP_AUTHORIZATION='Bearer '+ login_data.valid_token_unexisting_user)
        expected_dict = {
            "detail": "A user matching this token was not found."
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)

    def test_providing_invalid_token(self):
        response = self.client.post(self.url_user_detail,
            HTTP_AUTHORIZATION='Bearer j,asndg/lkbdsagdshmngj,asndg/lkbdsagdshmng')
        expected_dict = {
            "detail": "Error decoding signature. Please check the token you have provided."
            }
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.data, expected_dict)
