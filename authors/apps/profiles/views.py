from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer
from .models import Profile
from .renderers import ProfileRenderer
from .permissions import IsObjectOwner


class ProfileRetrieveUpdateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsObjectOwner, )
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileRenderer, )

    def get_object(self):
        return get_object_or_404(Profile, username=self.kwargs.get("username"))

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = request.data
        profile_data = data.get("profile", {}) if "profile" in data else data
        profile = self.get_object()
        # Enfornces custom permissions on profile object
        self.check_object_permissions(request, profile)
        serializer = self.serializer_class(profile,
                                           data=profile_data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
