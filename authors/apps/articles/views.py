from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from . import (
    serializers,
    models,
    permissions as custom_permissions
)
from .renderers import ArticleJSONRenderer, BookmarkJSONRenderer
from .utils.model_helpers import *
from ..profiles import models as profile_model

from .models import Rating, Article, Bookmark, ReadStats, Report
from .paginators import ArticleLimitOffsetPagination
from .utils.custom_filters import ArticleFilter
from authors.apps.notifications.tasks import send_email


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
        if not article:
            return Response({
                'errors': 'sorry article with that slug doesnot exist'
            }, status=status.HTTP_404_NOT_FOUND)
        serialized_data = self.serializer_class(article,
                                                context=context)
        # We try to add the user to the readstats of an article after they read
        # the article, but only if they are logged in and are not the authors
        # of the article.
        if not request.user.is_anonymous and\
                article.author.pk != request.user.pk:
            ReadStats.objects.get_or_create(
                user=request.user, article=article)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

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

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        rate = request.data.get('rate_score', {})
        if rate > 5 or rate < 1:
            return Response({
                'errors': 'Rate score should be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST)

        if article.author.pk == user.pk:
            message = 'Author can not rate their own article'
            data = {
                "title": article.title,
                "author": article.author.username,
                "average_ratings": article.average_ratings
            }
            return Response({'articles': data,
                             'message': message},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            Rating.objects.get(user=user.pk, article_id=article.pk)
            message = 'You already rated this article'
            data = {
                "title": article.title,
                "author": article.author.username,
                "average_ratings": article.average_ratings
            }
            return Response({'articles': data,
                             'message': message},
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


class BookmarkAPIView(generics.ListAPIView):
    """
    Class returns all articles in bookmarks of the user logged in
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.BookmarkSerializer
    renderer_classes = (BookmarkJSONRenderer,)

    def get_queryset(self):
        """
        This view should return a list of all the bookmarks
        for the currently authenticated user.
        """
        user = self.request.user
        return Bookmark.objects.filter(user=user)


class ArticleBookmarkAPIView(generics.GenericAPIView):
    """Class adds or deletes an article from users bookmarks"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.BookmarkSerializer

    def post(self, request, slug):
        """
        Add article to bookmarks of the user
        Checks to see article being added exists
        Checks to see if article has already been added to boomarks
        """
        article = get_single_article_using_slug(slug)
        if not article:
            error = f'An article with this slug,{slug}, does not exist'
            return Response({
                'error': error,
                'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND)
        user = request.user
        bookmark = get_single_bookmark_or_create_bookmark(article, user)

        if bookmark:
            return Response({
                'message': f'Article already exists in bookmarks',
                'status': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = f'Article has been added to bookmarks'
            return Response({
                'message': message,
                'status': status.HTTP_201_CREATED},
                status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        """
        Delete article from bookmarks of the user
        Checks to see article being deleted exists
        Checks to see if article has already been deleted from boomarks
        """
        article = get_single_article_using_slug(slug)
        if not article:
            return Response({
                'error': f'An article with this slug,{slug}, does not exist',
                'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND)
        user = request.user
        bookmark = get_single_bookmark_user(article, user)
        if bookmark:
            bookmark.delete()
            message = f'Article has been deleted from your bookmarks'
            return Response({
                'message': message,
                'status': status.HTTP_200_OK})
        else:
            error = f'This article does not exist in your bookmarks'
            return Response({
                'error': error,
                'status': status.HTTP_404_NOT_FOUND})


class ReportArticleAPIView(generics.GenericAPIView):
    """
    ReportArticleAPIView handles reporting of an article
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ArticleReporterSerializer

    def email_admin(self, article, request, reporter):
        """
        email_admin sends an email to the admin of the site when a report on
        an article has been made
        """
        article_url = reverse('articles:article-details',
                              kwargs={'slug': article.slug})
        article_url = request.build_absolute_uri(article_url)
        body = f"""Article {article_url} has been reported by
        {reporter.username} for the reason {request.data["reason"]}"""
        send_email.delay('Report Article', body, [settings.DEFAULT_FROM_EMAIL])

    def check_if_user_can_report(self, article, reporter):
        """
        check_if_user_can_report check's to see if a user is allowed to report
        an article
        """
        msg, status_code = None, None
        if not article:
            msg = "The article you're trying to report does not exist"
            status_code = status.HTTP_404_NOT_FOUND
        elif article.author == reporter:
            msg = "You cannot report your own article"
            status_code = status.HTTP_403_FORBIDDEN
        elif Report.objects.filter(reporter=reporter, article=article):
            msg = "You already reported this article"
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return msg, status_code

    def post(self, request, slug):
        article = get_single_article_using_slug(slug)
        reporter = request.user.profile
        msg, status_code = self.check_if_user_can_report(article, reporter)
        if msg:
            return Response({"message": msg}, status=status_code)
        context = {"request": request}
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(reporter=reporter, article=article)
        self.email_admin(article, request, reporter)
        msg = f"You have reported this article {article.title}"
        response_data = {"message": msg, "report": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)


class ReportsAPIView(generics.GenericAPIView):
    """
    ReportsAPIView retrieve's all the reports made if the user is an admin
    otherwise it retrieve's only the reports made by a particular logged in
    user
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ArticleReporterSerializer

    def get(self, request):
        if request.user.is_superuser:
            reports = models.Report.objects.all()
        else:
            user = request.user.profile
            reports = user.report_set.all()
        context = {"request": request}
        serializer = self.serializer_class(reports, many=True, context=context)
        response_data = {"reports": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)


class ReportAPIView(generics.GenericAPIView):
    """
    ReportAPIView retrieve's a single report. Only if a user created a report
    should they be able to retrieve the report or if they are an admin.
    """
    permission_classes = (permissions.IsAuthenticated,
                          custom_permissions.IsNotReportOwner,)
    serializer_class = serializers.ArticleReporterSerializer

    def get(self, request, id):
        reporter = request.user.profile
        report = get_single_report(id)
        if report:
            report = Report.objects.get(id=id)
            self.check_object_permissions(request, report)
            context = {"request": request}
            serializer = self.serializer_class(report, context=context)
            response_data = {"report": serializer.data}
            status_code = status.HTTP_200_OK
        else:
            response_data = {"message": "Report does not exist"}
            status_code = status.HTTP_404_NOT_FOUND
        return Response(response_data, status=status_code)
