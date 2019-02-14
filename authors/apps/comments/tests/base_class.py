from authors.apps.articles.tests import base_class
from authors.apps.comments.models import Comment
from authors.apps.profiles.models import Profile


class BaseTest(base_class.BaseTest):
    @staticmethod
    def create_comment(article, user):
        comment = Comment(body="Test Comment", article=article,
                          author=Profile.objects.get(user=user))
        comment.save()
        return comment
