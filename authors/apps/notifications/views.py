from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authors.apps.notifications.models import NotificationSettings, \
    Notification
from authors.apps.notifications.renderers import NotificationSettingsRenderer,\
    NotificationsRenderer
from authors.apps.notifications.serializers import \
    NotificationSettingsSerializer, NotificationSerializer


class NotificationSettingsAPIView(GenericAPIView):
    serializer_class = NotificationSettingsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (NotificationSettingsRenderer,)

    @staticmethod
    def get_notification_settings_object(user):
        """
        Get a user's notification settings object
        :param user: The user whose settings we are interested in
        :return: The notification settings
        """
        notification_settings, _ = NotificationSettings.objects.get_or_create(
            profile=user.profile)
        return notification_settings

    def get(self, request):
        """
        Get a user's notification settings
        :return: The json response with the settings
        """
        notification_settings = self.get_notification_settings_object(
            request.user)
        serializer = self.serializer_class(notification_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Update a user's notification settings
        :return: The result of the updated, successful or not
        """
        serializer = self.serializer_class(
            self.get_notification_settings_object(request.user),
            data=request.data,
            partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"notification_settings": serializer.data,
                         "message": "Settings updated"},
                        status=status.HTTP_200_OK)


class NotificationAPIView(GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (NotificationsRenderer,)

    def get(self, request):
        """
        Get all of a user's unread in-app notifications
        :return: The response containing these notifications
        """
        notifications = Notification.get_unread_in_app_notifications(
            request.user.profile)
        serializer = self.serializer_class(notifications, many=True)
        return Response({'notifications': serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        """
        Mark a user's in-appp notifications as read
        :return: Whether or not the action was successful
        """
        Notification.mark_all_unread_as_read(
            request.user.profile)
        message = "Marked all as read"
        return Response({'message': message}, status=status.HTTP_200_OK)
