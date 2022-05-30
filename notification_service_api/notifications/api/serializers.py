from rest_framework import serializers

from notification_service_api.notifications.models import Mailing, Operator, Tag


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
            "mailing_text",
            "tags",
            "operator_code",
        )
