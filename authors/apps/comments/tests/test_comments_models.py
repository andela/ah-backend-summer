from unittest.mock import MagicMock, patch

from authors.apps.comments.signals import CommentsSignalSender
from ...authentication.tests import base_class
from ..models import Comment, CommentReply
from ...profiles.models import Profile
from ...articles.models import Article
from .base_class import BaseTest as CommentsBaseTest
from .. import models
from ..utils import model_helpers


class TestCommentModel(base_class.BaseTest):
    """This class tests the Comments models __str__ method
    """

    def test_str_return_method_in_comment_model(self):
        self.create_comment()
        comment = Comment.objects.all().first()
        self.assertEqual(str(comment), 'i hate whales')

    def test_get_comment_using_id(self):
        comment = self.create_comment()
        response = model_helpers.get_single_comment_using_id(
            models.Comment,
            comment.id)
        self.assertIsNotNone(response)

    def test_get_comment_using_id_that_doesnot_exist(self):
        comment = self.create_comment()
        response = model_helpers.get_single_comment_using_id(
            models.Comment,
            comment.id+20)
        self.assertIsNone(response)

    def test_get_comment_edit_history_using_comment_id(self):
        comment = self.create_comment()
        response = model_helpers.get_comment_edit_history(
            models.Comment,
            comment.id)
        self.assertIsNotNone(response)
        self.assertIn('history_change_type', response[0])

    def test_get_comment_edit_history_when_comment_is_modified(self):
        comment = self.create_comment()
        comment.body = 'modified comment'
        comment.save()
        response = model_helpers.get_comment_edit_history(
            models.Comment,
            comment.id)
        self.assertEqual(2, len(response))
        self.assertIn('history_change_type', response[0])
        self.assertEqual(
            'modified',
            response[0]['history_change_type'])


class TestCommentReplyModel(base_class.BaseTest):
    """This class tests the Comments models __str__ method
    """

    def test_str_return_method_in_comment_model(self):
        user = self.activated_user()
        article = Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id)
        )

        comment = Comment.objects.create(
            body="biggest",
            author=Profile.objects.get(user=user.id),
            article=article
        )

        reply = CommentReply.objects.create(
            body="No jokes",
            author=Profile.objects.get(user=user.id),
            comment=comment
        )
        self.assertEqual(str(reply), 'No jokes')


class SignalTests(CommentsBaseTest):
    def test_new_comment_published_signal_emitted_on_new_comment(self):
        # mock this method, so we can track how it is called
        signal = 'authors.apps.comments.signals.comment_published_signal.send'
        with patch(signal) as comment_published_signal_mock:
            # it hasn't been called yet
            comment_published_signal_mock.assert_not_called()
            user = self.activated_user()
            article = self.create_article(user)
            # creating a comment should trigger it
            comment = self.create_comment(article,
                                          self.create_another_user_in_db())
            # it should have been called
            comment_published_signal_mock.assert_called_once_with(
                CommentsSignalSender,
                comment=comment)
