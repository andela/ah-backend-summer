from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

from . import (
    serializers,
    models,
    permissions as custom_permissions
)
from .renderers import ArticleJSONRenderer
from .utils import model_helpers
from ..profiles import models as profile_model


class ArticlesApiView (generics.ListCreateAPIView):
    """The ArticleDetailApiView handles the retreiving of a all article,
    and creation of a new article.
    """
    queryset = models.Article.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def post(self, request):
        data = request.data.get('articles')
        serializer = self.serializer_class(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=profile_model.Profile.objects.get(user=self.request.user)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailApiView (generics.GenericAPIView):
    """
    The ArticleDetailApiView handles the retreiving,
    updating (partially) and deleting of a single article
    """
    permission_classes = (custom_permissions.IsAuthorOfTheArticle,
                          permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def get_object(self, slug):
        article = model_helpers.get_single_article_using_slug(slug)
        return article

    def get(self, request, slug):
        article = self.get_object(slug)
        if article:
            serialized_data = self.serializer_class(article)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response({
            'errors': 'sorry article with that slug doesnot exist'
        }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        article = self.get_object(slug)
        if article:
            self.check_object_permissions(request, article)
            serializer_data = self.serializer_class(article,
                                                    request.data.get(
                                                        'articles'),
                                                    partial=True)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response(serializer_data.data,
                            status=status.HTTP_200_OK)
        return Response({
            'errors': 'sorry article with that slug doesnot exist'
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        article = self.get_object(slug)
        if article:
            self.check_object_permissions(request, article)
            article.delete()
            return Response({
                'article': 'Article has been deleted'},
                status=status.HTTP_200_OK
            )
        return Response({
            'errors': 'sorry article with that slug doesnot exist'
        }, status=status.HTTP_404_NOT_FOUND)
