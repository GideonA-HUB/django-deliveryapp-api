from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ConversationViewSet.as_view({'get': 'list'}), name='conversation_list'),
    path('<int:pk>/', views.ConversationViewSet.as_view({'get': 'retrieve'}), name='conversation_detail'),
    path('<int:conversation_id>/messages/', views.MessageViewSet.as_view({'get': 'list'}), name='message_list'),
    path('participants/', views.ConversationParticipantViewSet.as_view({'get': 'list'}), name='participant_list'),
    path('attachments/', views.MessageAttachmentViewSet.as_view({'get': 'list'}), name='attachment_list'),
] 