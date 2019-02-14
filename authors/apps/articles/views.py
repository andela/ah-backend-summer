from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from . import (
    serializers,
    models,
    permissions as custom_permissions
)
from .renderers import ArticleJSONRenderer
from .utils.model_helpers import *
from ..profiles import models as profile_model

from .models import Rating, Article
from .paginators import ArticleLimitOffsetPagination
from .utils.custom_filters import ArticleFilter


class ArticlesApiView (generics.ListCreateAPIView):
    """The ArticleDetailApiView handles the retreiving of a all article,
    and creation of a new article.
    """
    queryset = models.Article.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)
    pagination_class = ArticleLimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_class = ArticleFilter
    search_fields = ('author__username', 'description', 'body', 'title', )

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
        article = get_single_article_using_slug(slug)
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

    def patch(self, request, slug):
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
        article = get_single_article_using_slug(slug)

        if article and action is 'like':
            article.disliked_by.remove(request.user)
            article.liked_by.add(request.user)
            return Response({
                'message': 'You liked this article!'
            })

        if article and action is 'dislike':
            article.liked_by.remove(request.user)
            article.disliked_by.add(request.user)
            return Response({
                'message': 'You disliked this article!'
            })

        return Response({
            'errors': 'article with that slug does not exist'
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug='', action='like'):
        """
        Remove a user from the list of people that liked an article
        """
        article = get_single_article_using_slug(slug)

        if article and action is 'like':
            article.liked_by.remove(request.user)
            return Response({
                'message': 'You no longer like this article'
            })

        if article and action is 'dislike':
            article.disliked_by.remove(request.user)
            return Response({
                'message': 'You no longer dislike this article'
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
        article = get_single_article_using_slug(slug)

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


class FavoriteAPIView(generics.GenericAPIView):
    """
    FavoriteAPIView favorites an article
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ArticleSerializer

    def post(self, request, slug):
        data, status_code = favorite_unfavorite_article(request,
                                                        slug,
                                                        self.serializer_class,
                                                        True)
        return Response(data, status=status_code)


class UnFavoriteAPIView(generics.GenericAPIView):
    """
    UnFavoriteAPIView unfavorites an article
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ArticleSerializer

    def delete(self, request, slug):
        data, status_code = favorite_unfavorite_article(request,
                                                        slug,
                                                        self.serializer_class,
                                                        False)
        return Response(data, status=status_code)


class ArticleRatingAPIView(generics.GenericAPIView):
    """
    Allows user to rate an article.
    Restricts author from rating their own article
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ArticleRatingSerializer
    renderer_classes = (ArticleJSONRenderer,)

    def post(self, request, slug):
        """
        Allow user to rate an article
        :param request: The incoming request object
        :param slug: The expected article slug
        :return: article's rate score, title, author of that rated article
        """

        article = get_single_article_using_slug(slug)
        user = request.user

        rate = request.data.get('rate_score', {})
        if rate > 5 or rate < 1:
            return Response({
                'errors': 'Rate score should be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST)

        if article.author.pk == user.pk:
            return Response({
                'errors': 'Author can not rate their own article'},
                status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            Rating.objects.get(user=user.pk, article_id=article.pk)
            return Response(
                {'message': 'You already rated this article'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Rating.DoesNotExist:
            serializer.save(user=user, article=article)
            rate_data = serializer.data
            message = 'You have rated this article successfully'
            return Response({'articles': rate_data,
                             'message': message},
                            status=status.HTTP_201_CREATED)


class ArticleTagsApiView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        tags = get_all_available_tags()
        if tags:
            return Response(
                {'tags': list(tags)},
                status=status.HTTP_200_OK
            )
        msg = 'sorry no tags exist in the Database yet'
        return Response(
            {'tags': msg},
            status=status.HTTP_404_NOT_FOUND)
