from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer
from .models import Profile
from .permissions import IsObjectOwner


class ProfileRetrieveUpdateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsObjectOwner, )
    serializer_class = ProfileSerializer

    def get_object(self, username):
        try:
            profile = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            profile = None
        return profile

    def get(self, request, username):
        profile = self.get_object(username)
        if profile:
            serializer = self.serializer_class(profile)
            response_data = {"profile": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"error": "Profile with this username does not exist"},
                        status=status.HTTP_404_NOT_FOUND)

    def update(self, request, username):
        data = request.data
        profile_data = data.get("profile", {}) if "profile" in data else data
        profile = self.get_object(username)
        if profile:
            # Enfornces custom permissions on profile object
            self.check_object_permissions(request, profile)
            serializer = self.serializer_class(profile,
                                               data=profile_data,
                                               partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = "Your profile has been updated successfully."
            response_data = {"profile": serializer.data, "message": message}
            return Response(response_data, status=status.HTTP_200_OK)
        error_message = "Profile with this username does not exist"
        return Response({"errors": error_message},
                        status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username):
        return self.update(request, username)

    def patch(self, request, username):
        return self.update(request, username)
