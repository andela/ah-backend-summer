from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path('tags', views.ArticleTagsApiView.as_view(), name='tags'),
    path('<slug>/like', views.LikeDislikeArticleAPIView.as_view(),
         kwargs={'action': 'like'},
         name="like-article"),
    path('<slug>/dislike', views.LikeDislikeArticleAPIView.as_view(),
         kwargs={'action': 'dislike'},
         name="unlike-article"),
    path('<slug>/is-liked', views.ArticlesIsLikedDislikedAPIView.as_view(),
         kwargs={'action': 'like'},
         name="is-liked"),
    path('<slug>/is-disliked', views.ArticlesIsLikedDislikedAPIView.as_view(),
         kwargs={'action': 'dislike'},
         name="is-disliked"),
    path('', views.ArticlesApiView.as_view(),
         name='articles'),
    path('<slug>', views.ArticleDetailApiView.as_view(),
         name='article-details'),
    path('<slug>/favorite', views.FavoriteAPIView.as_view(),
         name='article-favorite'),
    path('<slug>/unfavorite', views.UnFavoriteAPIView.as_view(),
         name='article-unfavorite'),
    path('<slug>/rate', views.ArticleRatingAPIView.as_view(),
         name='article-rates'),
]
