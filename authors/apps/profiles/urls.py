from django.urls import path
from .views import (
    ProfileRetrieveUpdateView,
    ProfileFollowAPIView,
    ProfileFollowersAPIView,
    ProfileFollowingAPIView,
    UserProfileListAPIView,
    ReadStatsView
)

app_name = "profiles"

urlpatterns = [
    path("<username>", ProfileRetrieveUpdateView.as_view(),
         name="profile-detail-update"),
    path("<username>/follow", ProfileFollowAPIView.as_view(),
         name="follow"),
    path("follow/following", ProfileFollowingAPIView.as_view(),
         name="following"),
    path("follow/followers", ProfileFollowersAPIView.as_view(),
         name="followers"),
    path("", UserProfileListAPIView.as_view(),
         name="profile-list"),
    path('user/readstats', ReadStatsView.as_view(),
         name='read-stats'),
]
