from django.urls import reverse
from rest_framework import status
from authors.apps.authentication.models import User
from authors.apps.articles.models import Report
from ...authentication.tests.base_class import BaseTest
from .test_data.report_article_data import *


class TestReportArticle(BaseTest):
    def setUp(self):
        super().setUp()
        self.user = self.activated_user()
        self.article = self.create_article(self.user)
        self.url = reverse('articles:report-article',
                           kwargs={'slug': self.article.slug})
        self.reports_url = reverse('articles:reports')

    def create_article_using_different_user(self):
        """
        create_article_using_different_user creates an article using a
        different user
        """
        user = User.objects.create_user(username='oma',
                                        email='oma@email.com',
                                        password='pass1234')
        return self.create_article(user)

    def report_an_article(self):
        """
        report_an_article creates a report
        """
        article = self.create_article_using_different_user()
        return Report.objects.create(reporter=self.user.profile,
                                     article=article,
                                     reason="okay")

    def create_admin(self):
        """
        create_admin creates a superuser
        """
        return User.objects.create_superuser(username='admin',
                                             email='admin@email.com',
                                             password='pass1234')

    def test_user_cannot_report_article_which_does_not_exist(self):
        """
        Tests that a user cannot report an article that does not exist
        """
        self.client.force_authenticate(user=self.user)
        self.url = reverse('articles:report-article',
                           kwargs={'slug': 'jfdsgga'})
        response = self.client.post(self.url, data=valid_report_article_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"],
                         "The article you're trying to report does not exist")

    def test_user_cannot_report_their_article(self):
        """
        Tests that a user cannot report their article
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=valid_report_article_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"],
                         "You cannot report your own article")

    def test_same_user_cannot_report_same_article_twice(self):
        """
        Tests that a user cannot report the same article twice
        """
        article = self.create_article_using_different_user()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('articles:report-article',
                           kwargs={'slug': article.slug})
        self.client.post(self.url, data=valid_report_article_data)
        response = self.client.post(self.url, data=valid_report_article_data)
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data["message"],
                         "You already reported this article")

    def test_user_can_report_an_article(self):
        """
        Tests that a user can report an article
        """
        article = self.create_article_using_different_user()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('articles:report-article',
                           kwargs={'slug': article.slug})
        response = self.client.post(self.url, data=valid_report_article_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         f"You have reported this article {article.title}")

    def test_user_cannot_report_an_article_when_unauthenticated(self):
        """
        Tests that a user cannot report an article unless they are logged in
        """
        response = self.client.post(self.url, data=valid_report_article_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_report_an_article_without_reason(self):
        """
        Tests user cannot report an article without a reason
        """
        article = self.create_article_using_different_user()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('articles:report-article',
                           kwargs={'slug': article.slug})
        response = self.client.post(self.url, data=no_reason_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_retrieve_reports_they_made(self):
        """
        Tests that a user can retrieve the reports they have made
        """
        self.report_an_article()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.reports_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_reports_they_made_when_unauthenticated(self):
        """
        Tests user cannot retrieve reports they made unless they are
        authenticated
        """
        response = self.client.get(self.reports_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_retrieve_reports_made(self):
        """
        Tests admin can retrieve all reports users have made
        """
        report = self.report_an_article()
        admin = self.create_admin()
        self.client.force_authenticate(user=admin)
        response = self.client.get(self.reports_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_a_report_they_made(self):
        """
        Tests a user can retrieve a report they made
        """
        report = self.report_an_article()
        self.client.force_authenticate(user=self.user)
        report_url = reverse('articles:report', kwargs={'id': report.id})
        response = self.client.get(report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["report"]["reason"], report.reason)
        self.assertEqual(response.data["report"]["reporter"]["username"],
                         self.user.profile.username)

    def test_user_cant_retrieve_a_report_they_made_when_unauthenticated(self):
        """
        Test user cannot retrieve a report when they are unauthenticated
        """
        report = self.report_an_article()
        report_url = reverse('articles:report', kwargs={'id': report.id})
        response = self.client.get(report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_retrieve_a_report_they_didnt_make(self):
        """
        Tests a user cannot retrieve a report they didn't make
        """
        report = self.report_an_article()
        user = self.create_another_user_in_db()
        self.client.force_authenticate(user=user)
        report_url = reverse('articles:report', kwargs={'id': report.id})
        response = self.client.get(report_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_retrieve_a_single_report(self):
        """
        Tests admin can retrieve a single report
        """
        report = self.report_an_article()
        admin = self.create_admin()
        self.client.force_authenticate(user=admin)
        report_url = reverse('articles:report', kwargs={'id': report.id})
        response = self.client.get(report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["report"]["reason"], report.reason)
        self.assertEqual(response.data["report"]["reporter"]["username"],
                         self.user.profile.username)
