from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from notification_service_api.notifications.api.views import (
    ClientViewSet,
    MailingViewSet,
    MessageViewSet,
)
from notification_service_api.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("client", ClientViewSet)
router.register("mailing", MailingViewSet)
router.register("message", MessageViewSet)
router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
