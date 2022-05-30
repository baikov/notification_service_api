from rest_framework.viewsets import ModelViewSet

from notification_service_api.notifications.models import Client, Mailing

from .serializers import ClientSerializer, MailingSerializer


class MailingViewSet(ModelViewSet):
    # permission_classes = [AllowAny]
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
