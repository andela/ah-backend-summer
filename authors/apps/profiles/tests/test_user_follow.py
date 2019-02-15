import json
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from authors.apps.profiles.tests.test_data.profile_follow \
    import user1, user2, login_user1, login_user2, follow_user, not_a_user
from authors.apps.authentication.models import User


class TestFollowProfile(APITestCase):
    # Class to test all user follow functionality.
    def setUp(self):
        self.client = APIClient()
        username = follow_user['username']
        non_user = not_a_user['username']
        User.objects.create_user(**user1)
        User.objects.create_user(**user2)
        response = self.client.post(reverse("authentication:login"),
                                    data=json.dumps(login_user1),
                                    content_type="application/json")
        self.token1 = response.data.get("token")
        response = self.client.post(reverse("authentication:login"),
                                    data=json.dumps(login_user2),
                                    content_type="application/json")
        self.token2 = response.data.get("token")
        self.follow_url = reverse("profiles:follow", args=[username])
        self.follow_url2 = reverse("profiles:follow", args=[non_user])
        self.following_url = reverse('profiles:following')
        self.followers_url = reverse('profiles:followers')

    def test_follow_user(self):
        """ Test whether a user profile can follow another
        """
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['message'],
                         'You have followed ronnie')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_follow_if_unauthenticated(self):
        """ Test that a user cannot follow another if unauthenticated.
        """
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION='',)
        self.assertIn(response.data['detail'],
                      'Authentication credentials were not provided.')

    def test_user_cannot_follow_themself(self):
        """ Test that a user cannot follow themselves
        """
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token2}',)
        self.assertEqual(response.data['error'],
                         "You cannot follow yourself")
        self.assertEqual(response.data['status'], 422)

    def test_cannot_follow_non_existent_profile(self):
        """ Test that a user cannot follow a nonexistant user
        """
        response = self.client.post(
            self.follow_url2,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['errors']['error'],
                         'The Requested profile doesnot exist.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_follow_a_user_after_following_them(self):
        """ Test that a user cannot follow another user after following them
        """
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['message'],
                         'You have followed ronnie')
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['error'],
                         'You already followed ronnie')
        self.assertEqual(response.data['status'], 422)

    def test_unfollow_user(self):
        """ Test whether a user can unfollow another user
        """
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['message'],
                         'You have followed ronnie')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['message'],
                         'You have unfollowed ronnie')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_unfollow_non_existent_profile(self):
        """ Test that a user cannot unfollow a nonexistant user
        """
        response = self.client.delete(
            self.follow_url2,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['errors']['error'],
                         'The Requested profile doesnot exist.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_unfollow_themself(self):
        """ Test that a user cannot unfollow themselves
        """
        response = self.client.delete(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token2}',)
        self.assertEqual(response.data['error'],
                         "You cannot unfollow yourself")
        self.assertEqual(response.data['status'], 422)

    def test_user_cannot_unfollow_user_they_donnot_follow(self):
        """ Test that a user cannot unfollow another user they donnot follow
        """
        response = self.client.delete(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['error'],
                         'You are not following ronnie')
        self.assertEqual(response.data['status'], 422)

    def test_user_can_view_all_users_they_follow(self):
        """ Test that a user can view all users they are following.
        """
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['message'],
                         'You have followed ronnie')
        response = self.client.get(
            self.following_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['following'], ['ronnie'])
        self.assertEqual(response.data['status'], 200)

    def test_user_cannot_view_users_they_follow_if_they_follow_none(self):
        """ Test that a user cannot view users they are follow if they donnot
        follow any.
        """
        response = self.client.get(
            self.following_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['message'],
                         'You are not following anyone.')
        self.assertEqual(response.data['status'], 204)

    def test_user_can_view_all_users_who_follow_them(self):
        """ Test that a user can view all users that follow them.
        """
        response = self.client.post(
            self.follow_url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token1}',)
        self.assertEqual(response.data['message'],
                         'You have followed ronnie')
        response = self.client.get(
            self.followers_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token2}',)
        self.assertEqual(response.data['followers'], ['polos'])
        self.assertEqual(response.data['status'], 200)

    def test_user_cannot_view_followers_if_no_one_follows_them(self):
        """ Test that a user cannot view users who follow them
        if no one follows them.
        """
        response = self.client.get(
            self.followers_url,
            HTTP_AUTHORIZATION=f'Bearer {self.token2}',)
        self.assertEqual(response.data['message'],
                         'You have no followers.')
        self.assertEqual(response.data['status'], 204)
