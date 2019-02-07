from ...authentication.tests import base_class
from ..models import Article
from ...profiles.models import Profile


class TestArticleView(base_class.BaseTest):
    """This Test class tests the article models __str__ method
    """

    def test_str_return_method_in_article_model(self):
        user = self.activated_user()
        article = Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id))
        self.assertEqual(str(article), 'whale')
