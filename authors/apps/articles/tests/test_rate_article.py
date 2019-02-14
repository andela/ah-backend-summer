from django.urls import reverse
from rest_framework import status
from ...authentication.tests import base_class
from .test_data import test_rate_article_data
from ..models import Rating, Article
from ...profiles.models import Profile


class TestRatingModel(base_class.BaseTest):
    """
    This class tests the Rating View
    """

    def setUp(self):
        super().setUp()
        self.user_author = self.activated_user()
        self.client.force_authenticate(user=self.user_author)
        self.article = self.create_article(self.user_author)
        self.url_rate_article = reverse('articles:article-rates',
                                        kwargs={"slug": self.article.slug})
        self.url_articles = reverse('articles:articles')

    def create_article(self, user):
        return Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id))

    # unit tests for module under rating articles start here

    def test_rate_article_author(self):
        """
        Test rating an article fails when author tries to rate their
        own article
        """
        response = self.client.post(
            self.url_rate_article,
            data=test_rate_article_data.valid_rate_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Author can not rate their own article",
                      response.data.get('errors'))

    # integration tests for all modules under rating articles start here

    def test_rate_article_not_author(self):
        """
        Test rating an article passes when it's not author rating
        """
        self.user = self.create_another_user_in_db()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url_rate_article,
            data=test_rate_article_data.valid_rate_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rate_article_not_author_fails_invalid_rate(self):
        """
        Test rating an article fails when it's not author rating
        """
        self.user = self.create_another_user_in_db()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url_rate_article,
            data=test_rate_article_data.invalid_rate_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_article_not_author_rate_same_article(self):
        """
        Test rating an article passes but does not process request
        when it's not author rating
        an article they already rated
        """
        self.user = self.create_another_user_in_db()
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url_rate_article,
                         data=test_rate_article_data.valid_rate_data,
                         format='json')
        response = self.client.post(
            self.url_rate_article,
            data=test_rate_article_data.valid_rate_data,
            format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("You already rated this article",
                      response.data.get('message'))

    def test_get_rate_average(self):
        """
        Test rating an article passes when it's not author rating
        and returns average
        """
        self.user = self.create_another_user_in_db()
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url_rate_article,
                         data=test_rate_article_data.valid_rate_data,
                         format='json')
        response = self.client.get(self.url_articles,
                                   format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['average_ratings'], 2)
