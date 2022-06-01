from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from notification_service_api.notifications.models import Client, Mailing, Message

from .serializers import ClientSerializer, MailingSerializer, MessageSerializer


class MailingViewSet(ModelViewSet):
    # permission_classes = [AllowAny]
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, url_path="stats")
    def get_statistics(self, request, pk):
        mailing = Mailing.objects.get(id=pk)
        result = (
            mailing.messages.all()
            .values("status")
            .annotate(count=Count("mailing"))
            .order_by()
        )
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=True, url_path="msg")
    def get_messages(self, request, pk):
        mailing = Mailing.objects.get(id=pk)
        messages = mailing.messages.all()
        serializer = ListSerializer(
            child=MessageSerializer(), context=self.get_serializer_context()
        )
        return Response(
            serializer.to_representation(messages), status=status.HTTP_200_OK
        )


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
