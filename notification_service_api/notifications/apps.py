from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notification_service_api.notifications"

    def ready(self):
        try:
            import notification_service_api.notifications.signals  # noqa F401
        except ImportError:
            pass
