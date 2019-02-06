from rest_framework import status
from django.urls import reverse
from .base_test import BaseTest
from .test_data.profile_data import *
from authors.apps.authentication.tests.test_data.register_data \
    import valid_register_data


class TestRetrieveProfile(BaseTest):
    def test_retrieve_profile_succesfully(self):
        response = self.client.get(self.url,
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"],
                         valid_register_data["user"]["username"])

    def test_unauthenticated_user_cannot_retrieve_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_profile_that_does_not_exist(self):
        response = self.client.get("api/profiles/ajfgdjga")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Integration tests
    def test_can_retrieve_profile_for_different_user(self):
        self.client.post(reverse("authentication:register"),
                         data=another_user_register_data)
        username = another_user_register_data["username"]
        url = reverse("profiles:profile-detail-update",
                      kwargs={"username": username})
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], username)
