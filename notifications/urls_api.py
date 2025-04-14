from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationListView, NotificationDetailView,
    NotificationPreferencesView, MarkNotificationAsReadView,
    MarkAllNotificationsAsReadView
)

app_name = 'api-notifications'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/preferences/', NotificationPreferencesView.as_view(), name='notification-preferences'),
    path('notifications/<int:pk>/mark-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('notifications/mark-all-read/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-read'),
] 