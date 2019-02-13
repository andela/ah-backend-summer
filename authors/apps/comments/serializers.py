from rest_framework import serializers

from .models import Comment, CommentReply
from ..profiles import serializers as ProfileSerializers


class CommentSerializer(serializers.ModelSerializer):
    """This serializer class specifies fields to render to the user 
    for reteriving, updating or creating of a comment on an article.
    It specifies the author, article, created_at and updated_at fields
    as read-only since these fields data is auto generated
    """
    author = ProfileSerializers.ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "created_at",
            "updated_at",
            "body",
            "author",
            "article",
            "id"
        )
        read_only_fields = (
            "article",
            "author",
            "created_at",
            'updated_at'
            "id"
        )


class CommentReplySerializer(serializers.ModelSerializer):
    """This serializer class specifies fields to render to the user for
    reteriving,updating or creating of a reply to a comment. It specifies
    the author, comment,created_at and updated_at fields as read-only
    since these fields data is auto generated
    """
    author = ProfileSerializers.ProfileSerializer(read_only=True)

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
