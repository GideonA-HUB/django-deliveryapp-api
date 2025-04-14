from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification_detail'),
    path('preferences/', views.NotificationPreferencesView.as_view(), name='notification_preferences'),
    path('mark-read/<int:pk>/', views.MarkNotificationAsReadView.as_view(), name='mark_notification_read'),
    path('mark-all-read/', views.MarkAllNotificationsAsReadView.as_view(), name='mark_all_notifications_read'),
]
