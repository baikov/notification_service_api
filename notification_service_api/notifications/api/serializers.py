from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from notification_service_api.notifications.models import (
    Client,
    Mailing,
    Message,
    Operator,
    Tag,
)


class TagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Tag
        # fields = ["id", "name"]
        # extra_kwargs = {
        #     'name': {'validators': []},
        # }


class OperatorSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    name = serializers.CharField(required=False, max_length=50, allow_blank=True)

    class Meta:
        model = Operator
        # fields = ["id", "code", "name"]
        # extra_kwargs = {
        #     'code': {'validators': []},
        # }


class MailingSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    operators = OperatorSerializer(required=False, allow_null=True, many=True)

    class Meta:
        model = Mailing
        fields = (
            "id",
            "title",
            "start_datetime",
            "end_datetime",
            "text",
            "tags_logic",
            "tags",
            "operators",
        )

    def create(self, validated_data):
        operators_data = validated_data.pop("operators")
        tags_data = validated_data.pop("tags")
        operators_list = []
        if operators_data:
            for item in operators_data:
                try:
                    operator = Operator.objects.get(code=item["code"])
                    operators_list.append(operator)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(
                        {"code": "Такого оператора не существует в базе"}
                    )
        # else:
        #     operator = None
        tags_list = []
        for item in tags_data:
            try:
                tag = Tag.objects.get(name=item["name"])
                tags_list.append(tag)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    {"name": "Такого тега не существует в базе"}
                )
        mailing = Mailing.objects.create(**validated_data)
        mailing.tags.set(tags_list)
        mailing.operators.set(operators_list)
        return mailing


class ClientSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    operator_code = OperatorSerializer()

    class Meta:
        model = Client
        fields = ("id", "phone_number", "operator_code", "tags", "timezone")

    def create(self, validated_data):
        operator_data = validated_data.pop("operator_code")
        tags_data = validated_data.pop("tags")
        operator, _ = Operator.objects.get_or_create(**operator_data)
        tags_list = []
        for item in tags_data:
            obj, _ = Tag.objects.get_or_create(name=item["name"])
            tags_list.append(obj)
        client = Client.objects.create(operator_code=operator, **validated_data)
        client.tags.set(tags_list)
        return client


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "create_datetime", "status", "mailing", "client")
