from django.urls import path
from .views import (
    NotificationListView, NotificationDetailView,
    NotificationPreferencesView, MarkNotificationAsReadView,
    MarkAllNotificationsAsReadView
)

app_name = 'notifications'

urlpatterns = [
    # List all notifications
    path('', NotificationListView.as_view(), name='notification-list'),
    
    # Get notification details
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    
    # Notification preferences
    path('preferences/', NotificationPreferencesView.as_view(), name='notification-preferences'),
    
    # Mark notification as read
    path('<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    
    # Mark all notifications as read
    path('read-all/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-read'),
] 