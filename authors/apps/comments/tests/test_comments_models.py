from unittest.mock import MagicMock, patch

from authors.apps.comments.signals import CommentsSignalSender
from ...authentication.tests import base_class
from ..models import Comment, CommentReply
from ...profiles.models import Profile
from ...articles.models import Article
from .base_class import BaseTest as CommentsBaseTest


class TestCommentModel(base_class.BaseTest):
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
        self.assertEqual(str(comment), 'biggest')


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
