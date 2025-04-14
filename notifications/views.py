from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification, NotificationPreferences
from .serializers import NotificationSerializer, NotificationPreferencesSerializer

# Create your views here.

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationPreferencesView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        preferences, created = NotificationPreferences.objects.get_or_create(user=self.request.user)
        return preferences

class MarkNotificationAsReadView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)

class MarkAllNotificationsAsReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all notifications marked as read'}, status=status.HTTP_200_OK)
