from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
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
    path('<slug>/favorite', views.ToggleFavoriteAPIView.as_view(),
         name='article-favorite'),
]
