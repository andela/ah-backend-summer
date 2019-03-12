"""Test base class file containing setup"""
import json
from django.core import mail

from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data.login_data import (
    valid_login_data)
from .test_data.register_data import valid_register_data

from rest_framework.test import APITestCase, APIClient

from django.urls import reverse
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile
from authors.apps.comments.models import Comment


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.url_register = reverse('authentication:register')
        self.url_login = reverse('authentication:login')
        self.url_user_detail = reverse('authentication:retrieve-update')
        self.url_twitter = reverse('authentication:twitter-auth')
        self.url_google = reverse('authentication:google-auth')
        self.url_facebook = reverse('authentication:facebook-auth')

    def register_test_user(self):
        """
        Method that registers a test user
        """
        response = self.client.post(self.url_register, data=json.dumps(
            valid_register_data), content_type='application/json')
        return response

    def register_and_activate_test_user(self):
        """
        Method that registers a user and uses the outbox method of django's
        email services to access the sent email and extract the url from the
        sent link.
        """
        self.register_test_user()
        token = (mail.outbox[0].body.split("\n").pop(1).split(
            'email-verification/')[1])
        url = reverse('authentication:activate', args=[token])
        return self.client.get(url, content_type='application/json')

    def register_and_login_test_user(self):
        """
        Method that registers, activates and logs in a user,
        It then sets the received token into client's credentials.
        """
        self.register_and_activate_test_user()
        response = self.client.post(self.url_login, data=valid_login_data,
                                    format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def activated_user(self):
        """
        Method returns activated user who was verified
        """
        return User.objects.create_user(
            username='abc123',
            email='abc@abc.com',
            password='ia83naJS')

    def create_another_user_in_db(self):
        return User.objects.create_user(
            username='roger',
            email='roger@mail.com',
            password='ia83naJS')

    def create_article(self, user):
        return Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id))

    def create_comment(self):
        user = self.activated_user()
        article = self.create_article(user)
        return Comment.objects.create(
            body='i hate whales',
            author=Profile.objects.get(user=user.id),
            article=article
        )
