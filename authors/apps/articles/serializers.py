from rest_framework import serializers

from . import models
from ..profiles import serializers as ProfileSerializers
from .utils.utils import (get_article_read_time, get_articles_url,
                          get_sharing_links)


class ArticleSerializer (serializers.ModelSerializer):
    """The ArticleSerializer class is a model serializer class that
    specifies fields to render to the user for reteriving, updating
    or creating an article. It specifies only four read_only fields
    author field, slug field, created_at field and updated_at fields
    as these fields data is auto generated
    """
    author = ProfileSerializers.ProfileSerializer(read_only=True)
    favorited = serializers.SerializerMethodField()
    average_ratings = serializers.IntegerField(required=False)
    read_time = serializers.SerializerMethodField()
    share_links = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = (
            "slug",
            "title",
            "description",
            "created_at",
            "updated_at",
            "body",
            "author",
            "image",
            'like_count',
            'dislike_count',
            "favorited_by",
            "favoritesCount",
            "favorited",
            "average_ratings",
            "tag_list",
            "read_time",
            "share_links",
        )
        read_only_fields = (
            'author',
            'slug',
            'created_at',
            'updated_at'
            'like_count',
            'dislike_count',
        )

    def get_favorited(self, obj):
        """
        This method returns True is the logged in user favorited the article
        otherwise it returns False.
        """
        if self.context["request"].user.is_anonymous:
            return False
        if self.context["request"].user.profile in obj.favorited_by.all():
            return True
        return False
        extra_kwargs = {
            "author": {"read_only": True},
            "slug": {"read_only": True}
        }

    def get_read_time(self, obj):
        return get_article_read_time(obj.body)

    def get_share_links(self, obj):
        return get_sharing_links(obj, self.context['request'])


class ArticleRatingSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = models.Rating
        fields = (
            "rate_score", "title", "author"
        )
        extra_kwargs = {
            "rate_score": {"max_value": 5, "min_value": 1}
        }

    def get_title(self, obj):
        return obj.article.title

    def get_author(self, obj):
        return obj.article.author.user.username


class BookmarkSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    article_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Bookmark
        fields = (
            "slug", "title", "description", "author", "article_url"
        )

    def get_slug(self, obj):
        return obj.article.slug

    def get_description(self, obj):
        return obj.article.description

    def get_title(self, obj):
        return obj.article.title

    def get_author(self, obj):
        return obj.article.author.user.username

    def get_article_url(self, obj):
        return get_articles_url(obj, self.context['request'])
