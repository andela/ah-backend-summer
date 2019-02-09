from rest_framework import status

from authors.apps.articles.tests import base_class


class TestArticleAPIEndpoints(base_class.BaseTest):

    def setUp(self):
        super().setUp()
        self.user, self.article = self.create_article_and_authenticate_test_user()

    def test_user_can_undo_a_like(self):
        self.assertEqual(self.article.is_liked_by(self.user), False)
        response = self.client.post(self.like_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.is_liked_by(self.user), True)
        response = self.client.delete(self.like_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.is_liked_by(self.user), False)

    def test_user_can_undo_a_dislike(self):
        self.assertEqual(self.article.is_liked_by(self.user), False)
        response = self.client.post(self.dislike_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.is_disliked_by(self.user), True)
        response = self.client.delete(self.dislike_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.is_disliked_by(self.user), False)

    def test_like_then_dislike_undoes_the_like(self):
        self.article.liked_by.add(self.user)
        self.assertEqual(self.article.is_liked_by(self.user), True)
        self.assertEqual(self.article.is_disliked_by(self.user), False)
        response = self.client.post(self.dislike_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.is_liked_by(self.user), False)
        self.assertEqual(self.article.is_disliked_by(self.user), True)

    def test_dislike_then_like_undoes_the_dislike(self):
        self.article.disliked_by.add(self.user)
        self.assertEqual(self.article.is_disliked_by(self.user), True)
        self.assertEqual(self.article.is_liked_by(self.user), False)
        response = self.client.post(self.like_article_url(self.article.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.is_disliked_by(self.user), False)
        self.assertEqual(self.article.is_liked_by(self.user), True)

    def test_multiple_users_can_like_an_article(self):
        self.assertEqual(self.article.like_count, 0)
        # first like
        self.client.post(self.like_article_url(self.article.slug))
        self.assertEqual(self.article.like_count, 1)
        user2 = self.create_article_and_authenticate_test_user_2()
        self.client.force_authenticate(user2)
        # second like
        self.client.post(self.like_article_url(self.article.slug))
        self.assertEqual(self.article.like_count, 2)

    def test_user_can_the_number_of_people_that_liked_an_article(self):
        """a user can get an article's like count"""
        # first like
        self.client.post(self.like_article_url(self.article.slug))
        user2 = self.create_article_and_authenticate_test_user_2()
        self.client.force_authenticate(user2)
        # second like
        self.client.post(self.like_article_url(self.article.slug))
        response = self.client.get(self.article_url(self.article.slug))
        self.assertEqual(response.data['like_count'], 2)
