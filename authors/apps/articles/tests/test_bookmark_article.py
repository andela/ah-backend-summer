from django.urls import reverse
from rest_framework import status
from ...authentication.tests import base_class
from ..models import Article, Bookmark
from ...profiles.models import Profile


class TestBookmarkArticle(base_class.BaseTest):
    """
    This class tests the Bookmark Views
    """

    def setUp(self):
        super().setUp()
        self.user_author = self.activated_user()
        self.client.force_authenticate(user=self.user_author)
        self.article = self.create_article(self.user_author)
        self.url_bookmark = reverse('articles:article-bookmark',
                                    kwargs={"slug": self.article.slug})
        self.url_get_bookmark = reverse('bookmarks')
        self.url_articles = reverse('articles:articles')

    def test_add_article_to_bookmark(self):
        response = self.client.post(self.url_bookmark)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(response.data.get('message'),
                      'Article has been added to bookmarks')

    def test_add_article_to_bookmark_already_added(self):
        self.client.post(self.url_bookmark)
        response = self.client.post(self.url_bookmark)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(response.data.get('message'),
                      'Article already exists in bookmarks')

    def test_delete_article_from_bookmark(self):
        self.client.post(self.url_bookmark)
        response = self.client.delete(self.url_bookmark)
        self.assertIn(response.data.get('message'),
                      'Article has been deleted from your bookmarks')

    def test_delete_article_from_bookmark_already_deleted(self):
        self.client.post(self.url_bookmark)
        self.client.delete(self.url_bookmark)
        response = self.client.delete(self.url_bookmark)
        self.assertIn(response.data.get('error'),
                      'This article does not exist in your bookmarks')

    def test_retrieve_users_bookmarks(self):
        self.client.post(self.url_bookmark)
        response = self.client.get(self.url_get_bookmark)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Integration tests start here

    def test_add_to_bookmark_article_does_not_exist(self):
        article = Article.objects.all().first()
        self.client.delete(reverse('articles:article-details',
                                   kwargs={'slug': article.slug}),
                           format='json')
        response = self.client.post(self.url_bookmark)
        self.assertIn(response.data.get('error'),
                      f'An article with this slug,{article.slug}, \
does not exist')

    def test_delete_from_bookmark_article_does_not_exist(self):
        article = Article.objects.all().first()
        self.client.delete(reverse('articles:article-details',
                                   kwargs={'slug': article.slug}),
                           format='json')
        self.client.post(self.url_bookmark)
        response = self.client.delete(self.url_bookmark)
        self.assertIn(response.data.get('error'),
                      f'An article with this slug,{article.slug}, \
does not exist')
