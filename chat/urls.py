from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConversationViewSet, MessageViewSet,
    ConversationParticipantViewSet, MessageAttachmentViewSet
)

app_name = 'chat'

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'participants', ConversationParticipantViewSet, basename='participant')
router.register(r'attachments', MessageAttachmentViewSet, basename='attachment')

urlpatterns = [
    path('', include(router.urls)),
] 