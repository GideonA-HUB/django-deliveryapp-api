from rest_framework import serializers
from .models import Conversation, Message, ConversationParticipant, MessageAttachment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ConversationParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ConversationParticipant
        fields = ['id', 'user', 'joined_at', 'is_admin']

class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file', 'file_name', 'file_type', 'uploaded_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'created_at', 'updated_at', 'is_read', 'attachments']
        read_only_fields = ['sender', 'created_at', 'updated_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = ConversationParticipantSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'is_group', 'created_at', 'updated_at', 'participants', 'messages']
        read_only_fields = ['created_at', 'updated_at'] 