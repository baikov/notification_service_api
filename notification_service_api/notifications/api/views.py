from rest_framework.viewsets import ModelViewSet

from notification_service_api.notifications.models import Mailing

from .serializers import MailingSerializer


class MailingViewSet(ModelViewSet):
    # permission_classes = [AllowAny]
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
