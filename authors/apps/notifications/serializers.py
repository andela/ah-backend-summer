from rest_framework.serializers import ModelSerializer

from authors.apps.notifications.models import NotificationSettings, \
    Notification


class NotificationSettingsSerializer(ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = (
            'allow_in_app_notifications',
            'allow_email_notifications',
        )


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'pk',
            'title',
            'body',
        )
