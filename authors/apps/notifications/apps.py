from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'authors.apps.notifications'
    verbose_name = 'Notifications'

    def ready(self):
        from . import signals
