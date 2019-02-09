from rest_framework.reverse import reverse

from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile
from ...authentication.tests import base_class


class BaseTest(base_class.BaseTest):
    def setUp(self):
        super().setUp()
        self.articles_url = reverse('articles:articles')

    @staticmethod
    def article_url(slug):
        return reverse('articles:article-details', kwargs={'slug': slug})

    @staticmethod
    def like_article_url(slug):
        return reverse('articles:like-article', kwargs={'slug': slug})

    @staticmethod
    def dislike_article_url(slug):
        return reverse('articles:unlike-article', kwargs={'slug': slug})

    @staticmethod
    def is_liked_article_url(slug):
        return reverse('articles:is-liked', kwargs={'slug': slug})

    @staticmethod
    def is_disliked_article_url(slug):
        return reverse('articles:is-disliked', kwargs={'slug': slug})

    def create_article_and_authenticate_test_user(self):
        """
        This method create an article and force authenticates a user
        """
        user = self.activated_user()
        self.client.force_authenticate(user=user)
        return user, Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id))

    def create_article_and_authenticate_test_user_2(self):
        """
        This method create an article and force authenticates a different user
        """
        user2 = self.create_another_user_in_db()
        self.client.force_authenticate(user=user2)
        return user2
