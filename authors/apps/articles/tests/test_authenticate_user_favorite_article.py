from django.urls import reverse
from rest_framework import status
from authors.apps.authentication.tests import base_class


class TestToggleFavoriteArticle(base_class.BaseTest):
    """
    TestToggleFavoriteArticle handles testing for functionality to favourite
    and unfavourite articles
    """

    def setUp(self):
        super().setUp()
        self.user = self.activated_user()
        self.article = self.create_article(self.user)
        self.favorite_url = reverse('articles:article-favorite',
                                    kwargs={"slug": self.article.slug})
        self.unfavorite_url = reverse('articles:article-unfavorite',
                                      kwargs={"slug": self.article.slug})

    def test_user_can_favorite_article(self):
        """
        Test an authenticatated user can favourite an article
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.favorite_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["article"]["favorited"], True)
        self.assertEqual(response.data["article"]["favorited_by"][0],
                         self.user.id)
        self.assertEqual(response.data["article"]["favoritesCount"], 1)
        article_title = response.data["article"]["title"]
        self.assertEqual(response.data["message"],
                         f"You have favorited this article {article_title}")

    def test_user_can_unfavorite_article(self):
        """
        Test an authenticatated user can unfavourite an article
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.unfavorite_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["article"]["favorited"], False)
        self.assertEqual(response.data["article"]["favorited_by"], [])
        self.assertEqual(response.data["article"]["favoritesCount"], 0)
        article_title = response.data["article"]["title"]
        self.assertEqual(response.data["message"],
                         f"You have unfavorited this article {article_title}")

    def test_user_cannot_favorite_non_existing_article(self):
        """
        Test user cannot favourite an article that doesn't exist
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('articles:article-favorite',
                                            kwargs={"slug": "hjksgfjghs"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["errors"],
                         'Article with this slug doesnot exist')

    def test_user_cannot_unfavorite_non_existing_article(self):
        """
        Test user cannot unfavourite an article that doesn't exist
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('articles:article-unfavorite',
                                              kwargs={"slug": "hjksgfjghs"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["errors"],
                         'Article with this slug doesnot exist')

    def test_unauthenticated_user_cannot_favroite_article(self):
        """
        Test an unauthenticatated user cannot favourite an article
        """
        response = self.client.post(self.favorite_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_unfavroite_article(self):
        """
        Test an unauthenticatated user cannot unfavourite an article
        """
        response = self.client.post(self.unfavorite_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
