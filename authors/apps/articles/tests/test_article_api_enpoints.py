from django.urls import reverse

from rest_framework import status

from ...authentication.tests import base_class
from .test_data import test_article_data
from ..models import Article
from ...profiles.models import Profile


class TestArticleView(base_class.BaseTest):
    """
    This Test class tests the api endpoints for article
    it tests,
    1. get all articles
    2. get single article if authorized or not authorized
    3. delete an article if authorized or not authorized
    4. update an article if authorized or not authorized
    """

    def setUp(self):
        super().setUp()
        self.articles_url = reverse('articles:articles')

    def test_create_article(self):
        """
        This test method tests wether a user can create an article
        """
        self.register_and_login_test_user()
        response = self.client.post(self.articles_url,
                                    data=test_article_data.valid_article_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_article_if_user_is_not_authenticated(self):
        """
        This test method tests a user that is not authenticated tries to
        create an article. it tests the respnse status code and response
        message
        """
        response = self.client.post(self.articles_url,
                                    data=test_article_data.valid_article_data,
                                    format='json')
        expected_dict = {
            "detail": "Authentication credentials were not provided."
        }
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(expected_dict, response.data)

    def test_retrieve_get_articles_if_there_is_no_article_in_db(self):
        """
        This test method tests wether an empty list is returned if users
        try getting articles when the db (Database) is empty
        """
        response = self.client.get(self.articles_url)
        self.assertEqual([], response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_all_articles_if_the_db_is_not_empty(self):
        """
        This test method tests wether the returned list of articles is not
        empty an tests whether the valid expected data is returned
        """
        self.create_article_and_authenticate_test_user()
        response = self.client.get(self.articles_url)
        self.assertIn('title', response.data[0])
        self.assertIn('slug', response.data[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_article(self):
        """
        This test method tests wether the get single article endpoint returns
        valid data response
        """
        self.create_article_and_authenticate_test_user()
        article = Article.objects.all().first()
        response = self.client.get(reverse('articles:article-details',
                                           kwargs={'slug': article.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data)

    def test_retrieve_article_using_non_existing_slug(self):
        """
        This test method tests wether the get single article endpoint returns
        valid data response if a user tries getting an article of a slug that
        doesnot exist
        """
        response = self.client.get(reverse('articles:article-details',
                                           kwargs={'slug':
                                                   test_article_data.
                                                   un_existing_slug}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        expected_dict = {
            'errors': 'sorry article with that slug doesnot exist'}
        self.assertEqual(expected_dict, response.data)

    def test_update_an_article_authorized_user(self):
        """
        This test method tests wether the user updating an article is the
        one authorized to update the article
        """
        self.create_article_and_authenticate_test_user()
        article = Article.objects.all().first()
        response = self.client.put(reverse('articles:article-details',
                                           kwargs={'slug': article.slug}),
                                   data=test_article_data.update_article_data,
                                   format='json')
        self.assertIn('title', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_an_article_unauthorized_user(self):
        """
        This test method tests wether an unauthorized user tries to update
        an article that doesnot belong to them
        """
        self.create_article_and_authenticate_test_user_2()
        article = Article.objects.all().first()
        response = self.client.put(reverse('articles:article-details',
                                           kwargs={'slug': article.slug}),
                                   data=test_article_data.update_article_data,
                                   format='json')
        expected_dict_reponse = {
            'detail': 'This article does not belong to you. Access denied'}
        self.assertDictEqual(expected_dict_reponse, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_unexisting_article_slug(self):
        """
        This test method tests a user trying to update an article of a slug
        that doesnot exist
        """
        self.create_article_and_authenticate_test_user()
        article = Article.objects.all().first()
        response = self.client.put(reverse('articles:article-details',
                                           kwargs={'slug':
                                                   test_article_data.
                                                   un_existing_slug}),
                                   data=test_article_data.update_article_data,
                                   format='json')
        expected_dict = {
            'errors': 'sorry article with that slug doesnot exist'}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_article_authorized_user(self):
        self.create_article_and_authenticate_test_user()
        article = Article.objects.all().first()
        response = self.client.delete(reverse('articles:article-details',
                                              kwargs={'slug': article.slug}),
                                      format='json')
        expected_dict = {'article': 'Article has been deleted'}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_an_article_unauthorized_user(self):
        """
        This test method tests wether an unauthorized user tries to delete
        an article that doesnot belong to them
        """
        self.create_article_and_authenticate_test_user_2()
        article = Article.objects.all().first()
        response = self.client.delete(reverse('articles:article-details',
                                              kwargs={'slug': article.slug}),
                                      format='json')
        expected_dict_reponse = {
            'detail': 'This article does not belong to you. Access denied'}
        self.assertDictEqual(expected_dict_reponse, response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_an_article_when_user_is_authorized(self):
        """
        This test method tests a user trying to update an article of a slug
        that doesnot exist
        """
        self.create_article_and_authenticate_test_user()
        article = Article.objects.all().first()
        response = self.client.delete(reverse('articles:article-details',
                                              kwargs={'slug':
                                                      test_article_data.
                                                      un_existing_slug}),
                                      data=test_article_data.
                                      update_article_data,
                                      format='json')
        expected_dict = {
            'errors': 'sorry article with that slug doesnot exist'}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def create_article_and_authenticate_test_user(self):
        """
        This method create an article and force authenticates a user
        """
        user = self.activated_user()
        self.client.force_authenticate(user=user)
        Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id))

    def create_article_and_authenticate_test_user_2(self):
        """
        This method create an article and force authenticates a different user
        """
        self.create_article_and_authenticate_test_user()
        user2 = self.create_another_user_in_db()
        self.client.force_authenticate(user=user2)
