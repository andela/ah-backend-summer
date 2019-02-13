from django.urls import reverse
from rest_framework import status
from ...authentication.tests.base_class import BaseTest


class TestFilterSearchFunctionality(BaseTest):
    """
    TestFilterSearchFunctionality handles testing of the search and filter
    functionality of articles
    """
    def setUp(self):
        super().setUp()
        self.user = self.activated_user()
        self.client.force_authenticate(user=self.user)
        self.article = self.create_article(self.user)
        self.url = reverse('articles:articles')

    def add_tags_to_article(self):
        """
        add_tags_to_article method adds a tag to an article
        """
        self.article.tag_list = ["okay"]
        self.article.save()

    def test_user_can_filter_articles_by_author_username(self):
        """
        Test user can filter articles based on author username
        """
        username = self.user.username
        response = self.client.get(f"{self.url}?author={username}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?author=vdhfvsf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_user_can_filter_articles_by_title(self):
        """
        Test user can filter articles based on article title
        """
        title = self.article.title
        response = self.client.get(f"{self.url}?title={title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?title=vdhfvsf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_user_can_filter_articles_by_tag(self):
        """
        Test user can filter articles based on article tag
        """
        self.add_tags_to_article()
        tag = self.article.tag_list[0]
        response = self.client.get(f"{self.url}?tag={tag}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?tag=vdhfvsf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_user_can_filter_by_author_username_and_article_title(self):
        """
        Test user can filer for articles based on author username and article
        title
        """
        username = self.user.username
        title = self.article.title
        response = self.client.get(
            f"{self.url}?author={username}&title={title}"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?title=vfvsf&author={username}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
        response = self.client.get(f"{self.url}?title={title}&author=skjfg")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_user_can_filter_by_author_username_and_tag(self):
        """
        Test user can filer for articles based on author username and tag
        """
        self.add_tags_to_article()
        username = self.user.username
        tag = self.article.tag_list[0]
        response = self.client.get(
            f"{self.url}?author={username}&tag={tag}"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?tag=vfvsf&author={username}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
        response = self.client.get(f"{self.url}?tag={tag}&author=skjfg")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_user_can_filter_by_author_username_article_title_and_tag(self):
        """
        Test user can filer for articles based on author username, article
        title and tag
        """
        self.add_tags_to_article()
        username = self.user.username
        title = self.article.title
        tag = self.article.tag_list[0]
        response = self.client.get(
            f"{self.url}?author={username}&tag={tag}&title={title}"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(
            f"{self.url}?tag=vfvsf&author={username}&title={title}"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
        response = self.client.get(
            f"{self.url}?tag={tag}&author=skjfg&title={title}"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
        response = self.client.get(
            f"{self.url}?tag={tag}&author={username}&title=hjsdgfhj"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_user_can_search_for_articles_by_keywords(self):
        """
        Test user can search for articles based on keywords
        """
        username = self.user.username
        title = self.article.title
        description = self.article.description
        body = self.article.body
        response = self.client.get(f"{self.url}?search={username}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?search={title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?search={description}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?search={body}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(f"{self.url}?search=vdhfvsf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
