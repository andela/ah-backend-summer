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
        if self.context["request"].user.profile in obj.favorited_by.all():
            return True
        return False
