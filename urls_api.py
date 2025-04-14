from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import (
    OrderViewSet, OrderItemViewSet, OrderStatusViewSet,
    OrderPaymentViewSet, OrderTrackingViewSet
)
from services.views import (
    ServiceViewSet, ServiceOptionViewSet, ServiceCategoryViewSet,
    ServiceRatingViewSet, ServiceAvailabilityViewSet
)
from delivery.views import (
    DeliveryAssignmentViewSet, DeliveryLocationViewSet,
    DeliveryZoneViewSet, DeliveryViewSet, DeliveryTrackingViewSet,
    DeliveryRatingViewSet, ZoneBoundaryViewSet, DeliveryFeeViewSet
)
from notifications.views import (
    NotificationListView, NotificationDetailView,
    NotificationPreferencesView, MarkNotificationAsReadView,
    MarkAllNotificationsAsReadView
)
from chat.views import (
    ConversationViewSet, MessageViewSet,
    ConversationParticipantViewSet, MessageAttachmentViewSet
)

router = DefaultRouter()

# Orders URLs
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'order-status', OrderStatusViewSet, basename='order-status')
router.register(r'order-payments', OrderPaymentViewSet, basename='order-payment')
router.register(r'order-tracking', OrderTrackingViewSet, basename='order-tracking')

# Services URLs
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'service-options', ServiceOptionViewSet, basename='service-option')
router.register(r'service-categories', ServiceCategoryViewSet, basename='service-category')
router.register(r'service-ratings', ServiceRatingViewSet, basename='service-rating')
router.register(r'service-availability', ServiceAvailabilityViewSet, basename='service-availability')

# Delivery URLs
router.register(r'delivery-assignments', DeliveryAssignmentViewSet, basename='delivery-assignment')
router.register(r'delivery-locations', DeliveryLocationViewSet, basename='delivery-location')
router.register(r'delivery-zones', DeliveryZoneViewSet, basename='delivery-zone')
router.register(r'deliveries', DeliveryViewSet, basename='delivery')
router.register(r'delivery-tracking', DeliveryTrackingViewSet, basename='delivery-tracking')
router.register(r'delivery-ratings', DeliveryRatingViewSet, basename='delivery-rating')
router.register(r'zone-boundaries', ZoneBoundaryViewSet, basename='zone-boundary')
router.register(r'delivery-fees', DeliveryFeeViewSet, basename='delivery-fee')

# Chat URLs
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversation-participants', ConversationParticipantViewSet, basename='conversation-participant')
router.register(r'message-attachments', MessageAttachmentViewSet, basename='message-attachment')

urlpatterns = [
    path('', include(router.urls)),
    # Notifications URLs (using class-based views)
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/preferences/', NotificationPreferencesView.as_view(), name='notification-preferences'),
    path('notifications/<int:pk>/mark-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('notifications/mark-all-read/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-read'),
] 