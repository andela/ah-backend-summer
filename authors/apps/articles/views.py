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
        data = request.data
        article = data.get('articles') if "articles" in data else data
        serializer = self.serializer_class(
            data=article,
            context={"request": request}
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
        context = {"request": request}
        if article:
            serialized_data = self.serializer_class(article,
                                                    context=context)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response({
            'errors': 'sorry article with that slug doesnot exist'
        }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        data = request.data
        article_data = data.get('articles') if "articles" in data else data
        article = self.get_object(slug)
        context = {"request": request}
        if article:
            self.check_object_permissions(request, article)
            serializer_data = self.serializer_class(article,
                                                    article_data,
                                                    partial=True,
                                                    context=context)
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


class LikeDislikeArticleAPIView(generics.GenericAPIView):
    """
    Expose endpoints allowing a user to like an article and undo a like
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, slug='', action='like'):
        """
        Add a user to the list of people that liked an article
        :param action: the action- whether we are liking or disliking
        :param request: The incoming request object
        :param slug: The expected article slug
        :return: success for the action, or the appropriate error on failure
        """
        article = model_helpers.get_single_article_using_slug(slug)

        if article and action is 'like':
            article.disliked_by.remove(request.user)
            article.liked_by.add(request.user)
            return Response({
                'message': 'liked'
            })

        if article and action is 'dislike':
            article.liked_by.remove(request.user)
            article.disliked_by.add(request.user)
            return Response({
                'message': 'disliked'
            })

        return Response({
            'errors': 'article with that slug does not exist'
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug='', action='like'):
        """
        Remove a user from the list of people that liked an article
        """
        article = model_helpers.get_single_article_using_slug(slug)

        if article and action is 'like':
            article.liked_by.remove(request.user)
            return Response({
                'message': 'like undone'
            })

        if article and action is 'dislike':
            article.disliked_by.remove(request.user)
            return Response({
                'message': 'dislike undone'
            })

        return Response({
            'errors': 'article with that slug does not exist'
        }, status=status.HTTP_404_NOT_FOUND)


class ArticlesIsLikedDislikedAPIView(generics.GenericAPIView):
    """
    Expose endpoint checking if a the logged in user liked a particular article
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug='', action='like'):
        article = model_helpers.get_single_article_using_slug(slug)

        if article and action is 'like':
            return Response({
                'is_liked': article.is_liked_by(request.user)
            })

        if article and action is 'dislike':
            return Response({
                'is_disliked': article.is_disliked_by(request.user)
            })

        return Response({
            'errors': 'article with that slug does not exist'
        }, status=status.HTTP_404_NOT_FOUND)


class ToggleFavoriteAPIView(generics.GenericAPIView):
    """
    ToggleFavoriteAPIView favorites and unfavorites an article
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ArticleSerializer

    def get(self, request, slug):
        article = model_helpers.get_single_article_using_slug(slug)
        user = request.user.profile
        if article:
            message = models.Article.objects.toggle_favorite(user, article)
            serializer = self.serializer_class(article,
                                               context={"request": request})
            data = {"message": message, "article": serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        error_message = 'Sorry article with this slug doesnot exist'
        return Response({'errors': error_message},
                        status=status.HTTP_404_NOT_FOUND)
