from django.urls import reverse
from rest_framework import status
from . import base_class
from ..models import Article
from ...profiles.models import Profile


class TestReadStats(base_class.BaseTest):
    """
    This class tests the Read_stats View
    """

    def test_add_readstats_successfully(self):
        """
        Test that users can get their reading stats after viewing an article
        """
        self.create_article_and_authenticate_test_user()
        article_slug = Article.objects.latest('created_at').slug
        url = reverse('articles:article-details',
                      kwargs={'slug': f'{article_slug}'})

        self.create_article_and_authenticate_test_user_2()
        self.client.get(url,)

        username = Profile.objects.latest('created_at').username
        url2 = reverse('profiles:read-stats')
        response = self.client.get(url2,)
        self.assertEqual(response.data['user'], username)
        self.assertEqual(response.data['total_articles_read'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_get_readstats(self):
        """
        Test that anonymous users can not get reading stats
        """
        url2 = reverse('profiles:read-stats')
        response = self.client.get(url2)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN)
