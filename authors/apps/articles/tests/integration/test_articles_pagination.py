from django.urls import reverse

from rest_framework import status

from authors.apps.articles.tests import base_class
from ..test_data import test_article_data
from authors.apps.articles.models import Article


class TestArticleView(base_class.BaseTest):
    """
    This Test class tests the api endpoint of get all articles
    """

    def test_paginate_list_articles(self):
        """
        This test method tests whether the endpoint returns paginated articles
        """
        self.create_article_and_authenticate_test_user()
        response = self.client.get(self.articles_url)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
