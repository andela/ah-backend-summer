import json
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from authors.apps.authentication.tests.test_data.register_data \
    import valid_register_data
from authors.apps.authentication.tests.test_data.login_data \
    import valid_login_data
from authors.apps.authentication.models import User


class BaseTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        User.objects.create_user(
                                    username='abc123',
                                    email='abc@abc.com',
                                    password='ia83naJS')
        response = cls.client.post(reverse("authentication:login"),
                                   data=json.dumps(valid_login_data),
                                   content_type="application/json")
        cls.token = response.data.get("token")
        username = valid_register_data["user"]["username"]
        cls.url = reverse("profiles:profile-detail-update",
                          kwargs={"username": username})
