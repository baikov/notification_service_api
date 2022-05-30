from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# from notification_service_api.users.api.views import UserViewSet
from notification_service_api.notifications.api.views import (
    ClientViewSet,
    MailingViewSet,
    MessageViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)
router.register("client", ClientViewSet)
router.register("mailing", MailingViewSet)
router.register("message", MessageViewSet)


app_name = "api"
urlpatterns = router.urls
