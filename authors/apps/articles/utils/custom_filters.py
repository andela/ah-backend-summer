from django_filters import FilterSet, rest_framework
from ..models import Article


class ArticleFilter(FilterSet):
    """
    ArticleFilter is a custom filter class which will filter based on the
    article modeland the fields it will filter by are the article title,
    author username and tags.ArticleFilter also overides the filter fields
    lookup expressions from exact to icontains.
    """
    title = rest_framework.CharFilter('title',
                                      lookup_expr='icontains')
    author = rest_framework.CharFilter('author__username',
                                       lookup_expr='icontains')
    tag = rest_framework.CharFilter('tag_list',
                                    lookup_expr='icontains')
    favorited_by = rest_framework.CharFilter('favorited_by__username',
                                    lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ("title", "author", "tag", "favorited_by")
