from ...authentication.tests import base_class
from ..models import Comment, CommentReply
from ...profiles.models import Profile
from ...articles.models import Article


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
