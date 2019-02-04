from django.urls import path
from .views import ProfileRetrieveUpdateView

app_name = "profiles"

urlpatterns = [
    path("<username>/", ProfileRetrieveUpdateView.as_view(),
         name="profile-detail-update"),
]
