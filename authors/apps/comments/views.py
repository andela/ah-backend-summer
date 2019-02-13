from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer

from .serializers import CommentSerializer, CommentReplySerializer
from .models import Comment, CommentReply
from ..profiles.models import Profile
from ..articles.models import Article
from ..articles.utils import model_helpers


class CommentApiView (GenericAPIView):
    """
    The ApiView class handles the addition of a comment to an article
    and retrieving of all comments to an article.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    renderer_classes = (JSONRenderer,)

    def get_required_objects(self, request, slug):
        self.article = get_object_or_404(Article, slug=slug)
        self.data = request.data.get(
            'comment') if 'comment' in request.data else request.data

    def get_author_profile(self, request):
        self.author = Profile.objects.get(user=request.user)

    def get(self, request, slug):
        """Retrieve all comments on an article"""
        self.get_required_objects(request, slug)
        comments = Comment.objects.filter(article=self.article)
        serialized_data = self.serializer_class(comments, many=True)
        return Response({
            "comments": serialized_data.data,
            "commentCount": comments.count(),
            "status_message": (
            "Successfully returned comments on article: {}".format(slug)
            )},
            status=status.HTTP_200_OK
        )

    def post(self, request, slug):
        self.get_required_objects(request, slug)
        self.get_author_profile(request)
        serializer = self.serializer_class(
            data=self.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=self.author,
            article=self.article
        )
        return Response({"comment": serializer.data,
                         "message": (
                    "Successfully posted comment on article: {}".format(slug)
                         )},
                        status=status.HTTP_201_CREATED)


class CommentDetailApiView (GenericAPIView):
    """
    The CommentDetailApiView handles the retreiving, modification and 
    deletion of a single comment.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    renderer_classes = (JSONRenderer,)

    def get_required_objects(self, request, pk):
        self.comment = get_object_or_404(Comment, pk=pk)
        self.data = request.data.get(
            'comment') if 'comment' in request.data else request.data

    def get_author_profile(self, request):
        self.requester = Profile.objects.get(user=request.user)
        self.is_author = self.comment.author == self.requester

    def get(self, request, pk):
        """get the details of a comment"""
        self.get_required_objects(request, pk)
        serialized_data = self.serializer_class(self.comment)
        return Response({"comment": serialized_data.data,
                         "message": (
                    "Successfully returned details of comment: {}".format(pk)
                         )},
                        status=status.HTTP_200_OK)

    def patch(self, request, pk):
        self.get_required_objects(request, pk)
        self.get_author_profile(request)
        if not self.is_author:
            return Response({
                    "response": "You can only edit a comment you authored",
                            "status_message": "Failed: Access denied"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(
            self.comment, self.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"comment": serializer.data,
                    "message": "Successfully edited comment: {}".format(pk)},
                        status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        self.get_required_objects(request, pk)
        self.get_author_profile(request)
        if not self.is_author:
            return Response({
                    "response": "You can only delete a comment you authored",
                            "message": "Failed: Access denied"},
                            status=status.HTTP_403_FORBIDDEN)
        self.comment.delete()
        return Response({
            "message": "Successfully deleted comment: {}".format(pk)},
            status=status.HTTP_200_OK)


class CommentReplyApiView (GenericAPIView):
    """
    This ApiView class handles the addition of a reply to a comment
    and retrieving of all replies to that comment.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentReplySerializer
    renderer_classes = (JSONRenderer,)

    def get_required_objects(self, request, comment_pk):
        self.comment = get_object_or_404(Comment, pk=comment_pk)
        self.data = request.data.get(
            'reply') if 'reply' in request.data else request.data

    def get_author_profile(self, request):
        self.author = Profile.objects.get(user=request.user)

    def get(self, request, comment_pk):
        """Retrieve all replies on an comment"""
        self.get_required_objects(request, comment_pk)
        replies = CommentReply.objects.filter(comment=self.comment)
        serialized_data = self.serializer_class(replies, many=True)
        return Response({
            "replies": serialized_data.data,
            "repliesCount": replies.count(),
            "message": (
            "Successfully returned replies to comment: {}".format(comment_pk)
            )},
            status=status.HTTP_200_OK
        )

    def post(self, request, comment_pk):
        """Make a reply to a comment"""
        self.get_required_objects(request, comment_pk)
        self.get_author_profile(request)
        serializer = self.serializer_class(
            data=self.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=self.author,
            comment=self.comment
        )
        return Response({"reply": serializer.data,
                         "message": (
                "Successfully posted reply to comment: {}".format(comment_pk)
                         )},
                        status=status.HTTP_201_CREATED)


class CommentReplyDetailApiView (GenericAPIView):
    """
    The CommentReplyDetailApiView handles the retreiving, modification and 
    deletion of a single reply.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    renderer_classes = (JSONRenderer,)

    def get_required_objects(self, request, pk):
        self.reply = get_object_or_404(CommentReply, pk=pk)
        self.data = request.data.get(
            'reply') if 'reply' in request.data else request.data

    def get_author_profile(self, request):
        self.requester = Profile.objects.get(user=request.user)
        self.is_author = self.reply.author == self.requester

    def get(self, request, pk):
        self.get_required_objects(request, pk)
        """get the details of a reply"""
        serialized_data = self.serializer_class(self.reply)
        return Response({"reply": serialized_data.data,
                         "message": (
                    "Successfully returned details of reply: {}".format(pk)
                         )},
                        status=status.HTTP_200_OK)

    def patch(self, request, pk):
        self.get_required_objects(request, pk)
        self.get_author_profile(request)
        if not self.is_author:
            return Response({
                "response": "You can only edit a reply you authored",
                            "message": "Failed: Access denied"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(self.reply, self.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"reply": serializer.data,
                         "message": "Successfully edited reply: {}".format(pk)},
                        status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        self.get_required_objects(request, pk)
        self.get_author_profile(request)
        if not self.is_author:
            return Response({
                "response": "You can only delete a reply you authored",
                            "message": "Failed: Access denied"},
                            status=status.HTTP_403_FORBIDDEN)
        self.reply.delete()
        return Response({
            "message": "Successfully deleted reply: {}".format(pk)},
            status=status.HTTP_200_OK)
