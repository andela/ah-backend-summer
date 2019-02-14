from django.urls import path
from .views import NotificationSettingsAPIView, NotificationAPIView

app_name = "profiles"

urlpatterns = [
    path("settings", NotificationSettingsAPIView.as_view(),
         name="settings"),
    path("read", NotificationAPIView.as_view(), name="read"),
    path('', NotificationAPIView.as_view(), name="notifications"),
]
