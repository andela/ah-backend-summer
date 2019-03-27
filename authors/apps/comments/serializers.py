from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.apps.core import serializers as custom_serializers
from .models import Comment, CommentReply
from ..profiles import serializers as profile_serializers


class CommentSerializer(custom_serializers.ModelSerializer):
    """
    This serializer class specifies fields to render to the user
    for reteriving, updating or creating of a comment on an article.
    It specifies the author, article, created_at and updated_at fields
    as read-only since these fields data is auto generated
    """
    author = profile_serializers.ProfileSerializer(read_only=True)
    like_status = serializers.SerializerMethodField()
    dislike_status = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "created_at",
            "updated_at",
            "body",
            "author",
            "article",
            "id",
            'commenting_on',
            "like_count",
            "dislike_count",
            "like_status",
            "dislike_status"

        )
        read_only_fields = (
            "article",
            "author",
            "created_at",
            'updated_at',
            "id"
        )
        extra_kwargs = {
            'commenting_on': {
                'required': False
            }
        }

    def validate_commenting_on(self, data):
        if not data:
            raise ValidationError(
                "This field cannot be blank. "
                "If you are not commenting on "
                "a specific part of the article, "
                "exclude this field")
        if data not in self.context['article'].body:
            raise ValidationError(
                "You cannot comment on text not in the article"
            )

        return data

    def get_like_status(self, obj):
        """
        Check if the logged in user has liked the comment-
        """

        if self.context["request"].user.is_anonymous:
            return False
        if self.context["request"].user in obj.liked_by.all():
            return True
        return False

    def get_dislike_status(self, obj):
        """
       Check if the logged in user has disliked the comment
        """

        if self.context["request"].user.is_anonymous:
            return False
        if self.context["request"].user in obj.disliked_by.all():
            return True
        return False


class CommentReplySerializer(serializers.ModelSerializer):
    """
    This serializer class specifies fields to render to the user for
    reteriving,updating or creating of a reply to a comment. It specifies
    the author, comment,created_at and updated_at fields as read-only
    since these fields data is auto generated
    """
    author = profile_serializers.ProfileSerializer(read_only=True)

    class Meta:
        model = CommentReply
        fields = (
            "comment",
            "created_at",
            "updated_at",
            "body",
            "author",
            "id"
        )
        read_only_fields = (
            'author',
            'created_at',
            'updated_at',
            'comment',
            "id"
        )
