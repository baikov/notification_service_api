from rest_framework import serializers

from notification_service_api.notifications.models import (
    Client,
    Mailing,
    Message,
    Operator,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ["id", "code", "name"]


class MailingSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Mailing
        fields = (
            "id",
            "title",
            "start_datetime",
            "end_datetime",
            "text",
            "tags",
            "operator_code",
        )


class ClientSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Client
        fields = ("id", "phone_number", "operator_code", "tags", "timezone")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "create_datetime", "status", "mailing", "client")
