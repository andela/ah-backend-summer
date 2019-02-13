from ...authentication.tests import base_class
from ..models import Article
from ...profiles.models import Profile
from ..utils import model_helpers


class TestArticleModel(base_class.BaseTest):
    """This Test class tests the article models __str__ method
    """

    def test_str_return_method_in_article_model(self):
        article = self.create_article_using_models()
        self.assertEqual(str(article), 'whale')

    def test_get_all_tags_model_helper_if_no_article_exists(self):
        response = model_helpers.get_all_available_tags()
        self.assertIsNone(response)

    """ Intergration tests"""
    def test_get_all_tags_model_helper_if_author_tags_article(self):
        self.create_article_using_models()
        response = model_helpers.get_all_available_tags()
        self.assertEqual(response, {'cow', 'weed'})

    def test_get_all_tags_model_helper_if_author_doesnot_tag_article(self):
        response = model_helpers.get_all_available_tags()
        self.assertIsNone(response)

    def test_get_all_articles_with_same_tag_name_function(self):
        """
        This test method tests wether articles of the same tags would be
        retrieves
        """
        self.create_article_using_models()
        response = model_helpers.get_all_articles_with_same_tag_name('weed')
        self.assertIsNotNone(response)
        self.assertEqual(str(response[0]), 'whale')
        self.assertEqual(len(response), 1)

    def test_get_articles_using_tag_name_that_is_not_tagged_on_articles(self):
        """
        This test method tests wether articles of the same tags would be
        retrieves
        """
        self.create_article_using_models()
        response = model_helpers.get_all_articles_with_same_tag_name('weedd')
        self.assertIsNone(response)

    def test_get_articles_using_tag_name_when_no_articles_exist(self):
        """
        This test method tests wether articles of the same tags would be
        retrieves
        """
        response = model_helpers.get_all_articles_with_same_tag_name('weedd')
        self.assertIsNone(response)

    def create_article_using_models(self):
        user = self.activated_user()
        article = Article.objects.create(
            title='whale',
            description='fish',
            body='In water',
            author=Profile.objects.get(user=user.id),
            tag_list=['weed', 'cow'])
        return article
