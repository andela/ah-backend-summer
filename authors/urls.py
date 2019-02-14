"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from authors.apps.core.documentation import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('authors.apps.authentication.urls',
                            namespace='authentication')),
    path('api/v1/articles/', include('authors.apps.articles.urls',
                                     namespace='articles')),
    path('api/v1/comments/', include('authors.apps.comments.urls',
                                     namespace='comments')),
    path('api/v1/profiles/', include('authors.apps.profiles.urls',
                                     namespace='profiles')),
    path('api/v1/notifications/', include('authors.apps.notifications.urls',
                                          namespace='notifications')),
    path('', schema_view.with_ui('swagger'), name='schema-swagger-ui')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
