from django.urls import reverse

from rest_framework import status

from authors.apps.articles.tests import base_class
from .test_data import test_article_data
from ..models import Article


class TestArticleView(base_class.BaseTest):
    """
    This Test class tests the api endpoints for article
    it tests,
    1. get all articles
    2. get single article if authorized or not authorized
    3. delete an article if authorized or not authorized
    4. update an article if authorized or not authorized
    """

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
        response = self.client.patch(self.article_url(article.slug),
                                     data=test_article_data.
                                     update_article_data,
                                     format='json')
        self.assertIn('title', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_an_article_unauthorized_user(self):
        """
        This test method tests wether an unauthorized user tries to update
        an article that doesnot belong to them
        """
        self.create_article_and_authenticate_test_user()
        self.create_article_and_authenticate_test_user_2()
        article = Article.objects.all().first()
        response = self.client.patch(reverse('articles:article-details',
                                             kwargs={'slug': article.slug}),
                                     data=test_article_data.
                                     update_article_data,
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
        response = self.client.patch(reverse('articles:article-details',
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
        self.create_article_and_authenticate_test_user()
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

    def test_get_tags_when_none_exists(self):
        """
        Method tests when a user tries getting tags if no articles are tagged
        """
        self.create_article_and_authenticate_test_user()
        response = self.client.get(reverse('articles:tags'))
        expected_dict = {'tags': 'sorry no tags exist in the Database yet'}
        self.assertDictEqual(expected_dict, response.data)

    def create_article_and_authenticate_test_user(self):
        """
        This method create an article and force authenticates a user
        """
        user = self.activated_user()
        self.client.force_authenticate(user=user)
        self.create_article(user)


class TestArticleLikeDislikeArticleViews(base_class.BaseTest):
    def setUp(self):
        super().setUp()
        self.user, self.article = \
            self.create_article_and_authenticate_test_user()

    def test_user_can_like_an_article(self):
        """a user should be able to to like an article if authenticated"""
        self.assertFalse(self.article.is_liked_by(self.user))
        response = self.client.post(self.like_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.article.is_liked_by(self.user))

    def test_user_can_dislike_an_article(self):
        """a user should be able to to like an article if authenticated"""
        self.assertFalse(self.article.is_disliked_by(self.user))
        response = self.client.post(
            self.dislike_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.article.is_liked_by(self.user))

    def test_user_can_get_like_status_for_article_they_do_not_like(self):
        """a user should get the correct like status for an article they do
        not like"""
        response = self.client.get(
            self.is_liked_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_liked"], False)

    def test_user_can_get_like_status_for_article_they_like(self):
        """a user should get the correct like status for an article they do
        like"""
        self.article.liked_by.add(self.user)
        response = self.client.get(
            self.is_liked_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_liked"], True)

    def test_user_can_get_dislike_status_for_article_they_do_not_dislike(self):
        """a user should get the correct like status for an article they do
        not dislike"""
        response = self.client.get(
            self.is_disliked_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_disliked"], False)

    def test_user_can_get_dislike_status_for_article_they_dislike(self):
        """a user should get the correct like status for an article they do
        dislike"""
        self.article.disliked_by.add(self.user)
        response = self.client.get(
            self.is_disliked_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_disliked"], True)

    def test_unauthorized_user_cannot_like_an_article(self):
        """a request without a valid token does not allow a user to like an
        article"""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.like_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_dislike_an_article(self):
        """a request without a valid token does not allow a user to dislike an
        article"""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.dislike_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_the_number_of_people_that_liked_an_article(self):
        """a user can get an article's like count"""
        response = self.client.get(self.article_url(self.article.slug))
        # we haven't liked any article yet
        self.assertEqual(response.data['like_count'], 0)

    def test_user_can_the_number_of_people_that_disliked_an_article(self):
        """a user can get an article's dislike count"""
        response = self.client.get(self.article_url(self.article.slug))
        # we haven't disliked any article yet
        self.assertEqual(response.data['dislike_count'], 0)
