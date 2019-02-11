from rest_framework import serializers

from . import models
from ..profiles import serializers as ProfileSerializers


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
            "average_ratings"
        )
        read_only_fields = (
            'author',
            'slug',
            'created_at',
            'updated_at'
            'like_count',
            'dislike_count'
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
