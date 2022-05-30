from rest_framework import serializers

from notification_service_api.notifications.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
