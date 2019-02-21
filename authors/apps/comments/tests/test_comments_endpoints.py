from django.urls import reverse

from rest_framework import status

from ...authentication.tests import base_class
from ...authentication.models import User
from ..models import Comment, CommentReply
from ...profiles.models import Profile
from ...articles.models import Article
import json


class TestCommenting(base_class.BaseTest):

    def setUp(self):
        super().setUp()
        user = self.activated_user()
        Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id))
        self.article = Article.objects.all().first()
        self.slug = self.article.slug
        self.comments_url = reverse(
            'comments:comments', kwargs={'slug': self.slug})

    def authenticate_test_user1(self):
        user1 = User.objects.create_user(
            username='abcd123',
            email='def@abc.com',
            password='ia83naJS')
        self.client.force_authenticate(user=user1)

    def authenticate_test_user2(self):
        user2 = User.objects.create_user(
            username='abcd1234',
            email='ghi@abc.com',
            password='ia83naJS')
        self.client.force_authenticate(user=user2)

    def create_comment(self):
        self.authenticate_test_user1()
        self.comment = self.client.post(
            self.comments_url,
            data=json.dumps({"body": "very true"}),
            content_type='application/json'
        )
        self.comment_id = self.comment.data["comment"]["id"]
        self.reply_url = reverse(
            'comments:comment-reply', kwargs={'comment_pk': self.comment_id})

    def create_reply(self):
        self.reply = self.client.post(
            self.reply_url,
            data=json.dumps({"body": "indeed"}),
            content_type='application/json'
        )
        self.reply_id = self.reply.data["reply"]["id"]

    def test_user_can_view_comments_on_article_empty_db(self):
        self.authenticate_test_user1()
        response = self.client.get(
            self.comments_url,
            content_type='application/json'
        )
        self.assertEqual([], response.data["comments"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_logged_in_user_cannot_add_comment(self):
        response = self.client.post(
            self.comments_url,
            data=json.dumps({"body": "very true"}),
            content_type='application/json'
        )
        self.assertEqual("Authentication credentials were not provided.",
                         response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_add_comment(self):
        self.create_comment()
        self.assertEqual("very true", self.comment.data["comment"]["body"])
        self.assertEqual(self.comment.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_all_comments_on_article(self):
        self.create_comment()
        response = self.client.get(
            self.comments_url, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_comment_details(self):
        self.create_comment()
        response = self.client.get(
            reverse("comments:comment-details",
                    kwargs={"pk": self.comment_id}),
            content_type='application/json'
        )
        self.assertEqual("very true", response.data["comment"]['body'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_edit_comment_if_you_authored_it(self):
        self.create_comment()
        response = self.client.patch(
            reverse("comments:comment-details",
                    kwargs={"pk": self.comment_id}),
            data=json.dumps({"body": "very true indeed!"}),
            content_type='application/json'
        )
        self.assertEqual("very true indeed!", response.data["comment"]["body"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_edit_comment_if_you_didnt_author_it(self):
        self.create_comment()
        self.authenticate_test_user2()
        response = self.client.patch(
            reverse("comments:comment-details",
                    kwargs={"pk": self.comment_id}),
            data=json.dumps({"body": "very true indeed!"}),
            content_type='application/json'
        )
        self.assertEqual(
            "You can only edit a comment you authored",
            response.data['response'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_comment_if_you_authored_it(self):
        self.create_comment()
        response = self.client.delete(
            reverse("comments:comment-details",
                    kwargs={"pk": self.comment_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_delete_comment_if_you_didnt_author_it(self):
        self.create_comment()
        self.authenticate_test_user2()
        response = self.client.delete(
            reverse("comments:comment-details",
                    kwargs={"pk": self.comment_id}),
            content_type='application/json'
        )
        self.assertEqual(
            "You can only delete a comment you authored",
            response.data['response'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_view_replies_on_comment_empty_db(self):
        self.create_comment()
        response = self.client.get(
            self.reply_url,
            content_type='application/json'
        )
        self.assertEqual([], response.data["replies"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_logged_in_user_cannot_add_reply(self):
        response = self.client.post(
            reverse('comments:comment-reply', kwargs={'comment_pk': 1}),
            data=json.dumps({"body": "indeed!"}),
            content_type='application/json'
        )
        self.assertEqual("Authentication credentials were not provided.",
                         response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_add_reply(self):
        self.create_comment()
        self.create_reply()
        self.assertEqual("indeed", self.reply.data["reply"]["body"])
        self.assertEqual(self.comment.status_code, status.HTTP_201_CREATED)

    def test_user_can_get_all_replies_on_comment(self):
        self.create_comment()
        self.create_reply()
        response = self.client.get(
            self.reply_url, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_reply_details(self):
        self.create_comment()
        self.create_reply()
        response = self.client.get(
            reverse("comments:comment-reply-details",
                    kwargs={"pk": self.reply_id}),
            content_type='application/json'
        )
        self.assertEqual("indeed", response.data["reply"]['body'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_edit_reply_if_you_authored_it(self):
        self.create_comment()
        self.create_reply()
        response = self.client.patch(
            reverse("comments:comment-reply-details",
                    kwargs={"pk": self.reply_id}),
            data=json.dumps({"body": "i disagree"}),
            content_type='application/json'
        )
        self.assertEqual("i disagree", response.data["reply"]["body"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_edit_reply_if_you_didnt_author_it(self):
        self.create_comment()
        self.create_reply()
        self.authenticate_test_user2()
        response = self.client.patch(
            reverse("comments:comment-reply-details",
                    kwargs={"pk": self.reply_id}),
            data=json.dumps({"body": "i disagree"}),
            content_type='application/json'
        )
        self.assertEqual("You can only edit a reply you authored",
                         response.data['response'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_reply_if_you_authored_it(self):
        self.create_comment()
        self.create_reply()
        response = self.client.delete(
            reverse("comments:comment-reply-details",
                    kwargs={"pk": self.reply_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_delete_reply_if_you_didnt_author_it(self):
        self.create_comment()
        self.create_reply()
        self.authenticate_test_user2()
        response = self.client.delete(
            reverse("comments:comment-reply-details",
                    kwargs={"pk": self.reply_id}),
            content_type='application/json'
        )
        self.assertEqual(
            "You can only delete a reply you authored",
            response.data['response'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_edit_history_if_slug_is_invalid(self):
        self.create_comment()
        comment = Comment.objects.all().first()
        self.authenticate_test_user2()
        response = self.client.get(
            reverse("comments:comment-edit-history",
                    kwargs={
                        "slug": "wrong_slug",
                        "pk": comment.id}),
            content_type='application/json'
        )
        expected_dict = {
            "error": "Article with slug 'wrong_slug' doesnot exist",
            "status": 404
        }
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_get_edit_history_if_comment_id_that_doesnt_exist(self):
        user = self.create_another_user_in_db()
        self.create_article(user)
        article = Article.objects.all().first()
        self.authenticate_test_user2()
        response = self.client.get(
            reverse("comments:comment-edit-history",
                    kwargs={
                        "slug": article.slug,
                        "pk": 5}),
            content_type='application/json'
        )
        expected_dict = {
            "error": "Comment with id '5' doesnot exist",
            "status": 404
        }
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_get_edit_history_for_comment_with_valid_slug_article_and_id(self):
        self.create_comment()
        comment = Comment.objects.all().first()
        article = Article.objects.all().first()
        response = self.client.get(
            reverse("comments:comment-edit-history",
                    kwargs={"slug": article.slug,
                            "pk": comment.id}),
            content_type='application/json'
        )
        self.assertIn('history_change_type', response.data['history'][0])
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_get_edit_history_for_comment_reply_with_invalid_comment_id(self):
        """
        this method tests whether an error response of an invalid comment id is
        returned if user gets reply edit history for using a comment id that
        doesnot exist
        """
        self.create_comment()
        self.create_reply()
        comment_reply = CommentReply.objects.all().first()
        response = self.client.get(
            reverse("comments:comment-reply-edit-history",
                    kwargs={
                        "comment_pk": 5,
                        "pk": comment_reply.id}),
            content_type='application/json'
        )
        expected_dict = {
            "error": "Comment with id '5' doesnot exist",
            "status": 404}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_get_edit_history_for_comment_reply_id_that_doesnt_exist(self):
        """
        this method tests whether an error response of an invalid comment id is
        returned if user gets reply edit history using a comment reply id that
        doesnot exist
        """
        self.create_comment()
        comment = Comment.objects.all().first()
        response = self.client.get(
            reverse("comments:comment-reply-edit-history",
                    kwargs={"comment_pk": comment.id,
                            "pk": 5}),
            content_type='application/json'
        )
        expected_dict = {
            "error": "Comment reply with id '5' doesnot exist",
            "status": 404}
        self.assertDictEqual(expected_dict, response.data)
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_get_edit_history_for_comment_reply_with_valid_id(self):
        """this method tests for status code and response returned if user
        suppliesa valid comment and comment reply id
        """
        self.create_comment()
        self.create_reply()
        comment_reply = CommentReply.objects.all().first()
        comment = Comment.objects.all().first()
        response = self.client.get(
            reverse("comments:comment-reply-edit-history",
                    kwargs={"comment_pk": comment.id,
                            "pk": comment_reply.id}),
            content_type='application/json'
        )
        self.assertIn('history_change_type', response.data['history'][0])
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
