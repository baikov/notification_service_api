from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from notification_service_api.notifications.models import Client, Mailing, Message

from .serializers import ClientSerializer, MailingSerializer, MessageSerializer


class MailingViewSet(ModelViewSet):
    # permission_classes = [AllowAny]
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
