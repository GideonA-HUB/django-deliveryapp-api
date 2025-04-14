from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, ConversationParticipant, MessageAttachment
from .serializers import (
    ConversationSerializer, MessageSerializer,
    ConversationParticipantSerializer, MessageAttachmentSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants__user=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        conversation = self.get_object()
        participants = conversation.participants.all()
        serializer = ConversationParticipantSerializer(participants, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants__user=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        conversation = get_object_or_404(Conversation, id=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)

class ConversationParticipantViewSet(viewsets.ModelViewSet):
    queryset = ConversationParticipant.objects.all()
    serializer_class = ConversationParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ConversationParticipant.objects.filter(user=self.request.user)

class MessageAttachmentViewSet(viewsets.ModelViewSet):
    queryset = MessageAttachment.objects.all()
    serializer_class = MessageAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MessageAttachment.objects.filter(message__conversation__participants__user=self.request.user) 