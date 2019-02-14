from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class NotificationSettingsRenderer(JSONRenderer):
    """The ArticleJSONRenderer returns a Json object of notifications
        """
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        message = "Notification Settings Ready" if 'errors' not in data \
            else "Failed to get notification Settings"
        if 'message' not in data:
            data['message'] = message
        return json.dumps(data)


class NotificationsRenderer(JSONRenderer):
    """The ArticleJSONRenderer returns a Json object of notifications
        """
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        if 'message' not in data:
            if 'errors' in data or 'notifications' not in data:
                message = "Failed to get notifications"
                data['message'] = message
            else:
                if 'message' not in data:
                    message = "Notifications Ready"
                    data['message'] = message

        return json.dumps(data)
