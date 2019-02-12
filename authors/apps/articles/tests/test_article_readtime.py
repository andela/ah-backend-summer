from rest_framework import status
from authors.apps.articles.tests import base_class
from ..utils.utils import get_article_read_time
from .test_data import test_article_data


class TestArticleReadTime(base_class.BaseTest):
    """Class tests calculation of read time of an article"""

    def test_calculate_readtime(self):
        read_time = get_article_read_time(
            test_article_data.one_min_read_text
        )
        self.assertIn("1 min read", read_time)

    def test_calculate_readtime_empty_body(self):
        read_time = get_article_read_time(
            test_article_data.zero_min_read_text
        )
        self.assertIn("0 min read", read_time)
