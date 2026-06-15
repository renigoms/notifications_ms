from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'create_at']
        read_only_fields = ['id','create_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar notificações via API.
    Recebe user_id e message. O target é resolvido automáticamente
    a partir do X-Api-Key (empresa) + user_id do body.
    """

    user_id = serializers.IntegerField()
    message = serializers.CharField()
