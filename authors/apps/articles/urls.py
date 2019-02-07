from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path('', views.ArticlesApiView.as_view(),
         name='articles'),
    path('<slug>', views.ArticleDetailApiView.as_view(),
         name='article-details'),
]
