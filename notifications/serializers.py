from rest_framework import serializers
from .models import Notification, NotificationPreferences

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'notification_type', 'is_read', 'created_at']
        read_only_fields = ['user', 'created_at']

class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        fields = [
            'id', 'user', 'email_notifications', 'push_notifications', 'sms_notifications',
            'order_updates', 'promotional_updates', 'newsletter', 'quiet_hours_start',
            'quiet_hours_end', 'notification_frequency'
        ]
        read_only_fields = ['user'] 