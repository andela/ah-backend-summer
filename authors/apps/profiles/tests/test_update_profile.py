import json
from rest_framework import status
from django.urls import reverse
from .test_data.profile_data import *
from .base_test import BaseTest


class TestUpdateProfile(BaseTest):
    def test_patch_profile_successfully(self):
        response = self.client.put(self.url,
                                   data=json.dumps(valid_partial_profile_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["bio"],
                         valid_partial_profile_data["bio"])
        self.assertEqual(response.data["profile"]["first_name"], None)
        self.assertEqual(response.data["profile"]["last_name"], None)

    def test_update_profile_successfully(self):
        response = self.client.put(self.url,
                                   data=valid_profile_data,
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["username"],
                         valid_profile_data["username"])
        self.assertEqual(response.data["profile"]["bio"],
                         valid_profile_data["bio"])
        self.assertEqual(response.data["profile"]["first_name"],
                         valid_profile_data["first_name"])
        self.assertEqual(response.data["profile"]["last_name"],
                         valid_profile_data["last_name"])

    def test_cannot_update_profile_when_unauthenticated(self):
        response = self.client.put(self.url,
                                   data=json.dumps(valid_partial_profile_data),
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_profile_with_no_username(self):
        response = self.client.put(self.url,
                                   data=json.dumps(no_username_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["username"][0],
                         no_username_error)

    def test_cannot_update_profile_with_no_image(self):
        response = self.client.put(self.url,
                                   data=json.dumps(no_image_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["image"][0], no_image_error)

    def test_cannot_update_profile_with_no_username_no_image(self):
        response = self.client.put(self.url,
                                   data=json.dumps(no_image_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["image"][0], no_image_error)

    def test_user_cannot_update_profile_that_doesnot_exist(self):
        response = self.client.put(reverse("profiles:profile-detail-update",
                                           kwargs={"username": "jsdvjs"}),
                                   data=json.dumps(valid_partial_profile_data),
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["errors"],
                         "Profile with this username does not exist")

    def test_user_cannot_update_profile_with_non_profile_fields(self):
        response = self.client.put(self.url,
                                   data=non_profile_fields_data,
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["error"][0],
                         "Please only provide the profile fields")

    # Integration tests
    def test_cannot_update_profile_for_different_user(self):
        self.client.post(reverse("authentication:register"),
                         data=json.dumps(another_user_register_data),
                         content_type="application/json")
        username = another_user_register_data["username"]
        url = reverse("profiles:profile-detail-update",
                      kwargs={"username": username})
        response = self.client.put(url,
                                   data=json.dumps(valid_partial_profile_data),
                                   content_type="application/json",
                                   HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
