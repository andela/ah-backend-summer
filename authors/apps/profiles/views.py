from rest_framework import generics, status, permissions
from rest_framework.response import Response

from authors.apps.authentication.models import User
from authors.apps.profiles.exceptions import ProfileDoesNotExist
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
            serializer = self.serializer_class(profile, context={
                'request': request
            })
            response_data = {"profile": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({
            "error": "Profile with this username does not exist",
            "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

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
            response_data = {
                "profile": serializer.data,
                "message": message,
                "status": status.HTTP_200_OK}
            return Response(response_data, status=status.HTTP_200_OK)
        error_message = "Profile with this username does not exist"
        return Response({
            "errors": error_message,
            "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username):
        return self.update(request, username)

    def patch(self, request, username):
        return self.update(request, username)


class ProfileFollowAPIView(generics.GenericAPIView):
    # Views for following and unfollowing.
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def post(self, request, username=None):
        # View Method to follow a user profile
        follower = self.request.user.profile
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        if follower == followee:
            return Response({
                "error": "You cannot follow yourself",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if followee not in follower.follows.all():
            follower.follow(followee)
            message = f'You have followed {followee}'
            serializer = self.serializer_class(followee, context={
                'request': request})
            response_data = {
                "message": message,
                "profile": serializer.data,
                "status": status.HTTP_200_OK}
            return Response(response_data, status=status.HTTP_200_OK)
        error_msg = f'You already followed {followee}'
        return Response({
            "error": error_msg,
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, username=None):
        # View Method to unfollow a user profile
        follower = self.request.user.profile
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        if follower == followee:
            return Response({
                "error": "You cannot unfollow yourself",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if followee in follower.follows.all():
            follower.unfollow(followee)
            message = f'You have unfollowed {followee}'
            serializer = self.serializer_class(followee, context={
                'request': request})
            response_data = {
                "message": message,
                "profile": serializer.data,
                "status": status.HTTP_200_OK}
            return Response(response_data, status=status.HTTP_200_OK)
        error_msg = f'You are not following {followee}'
        return Response({
            "error": error_msg,
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProfileFollowingAPIView(generics.GenericAPIView):
    # This class returns a list of profiles a user is following.
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        profile = user.profile
        queryset = Profile.objects.get(user__email=user).follows.all()

        following = []
        for followee in queryset:
            followee_name = User.objects.get(username=followee)
            followee_username = followee_name.username
            following.append(followee_username)
        if following is None or following == []:
            msg = {
                'message': 'You are not following anyone.',
                'status': status.HTTP_204_NO_CONTENT}
            return Response(data=msg, status=status.HTTP_204_NO_CONTENT)
        msg = {
            'following': following,
            'status': status.HTTP_200_OK}
        return Response(data=msg, status=status.HTTP_200_OK)


class ProfileFollowersAPIView(generics.GenericAPIView):
    # This class returns a list of profiles that follow a user.
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        profile = user.profile
        queryset = Profile.objects.get(user__email=user).followed_by.all()

        followers = []
        for follower in queryset:
            follower_name = User.objects.get(username=follower)
            follower_username = follower_name.username
            followers.append(follower_username)
        if followers is None or followers == []:
            msg = {
                'message': 'You have no followers.',
                'status': status.HTTP_204_NO_CONTENT}
            return Response(data=msg, status=status.HTTP_204_NO_CONTENT)
        msg = {
            'followers': followers,
            'status': status.HTTP_200_OK}
        return Response(data=msg, status=status.HTTP_200_OK)
