from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    OrderItemViewSet,
    OrderStatusViewSet,
    OrderPaymentViewSet,
    OrderTrackingViewSet,
)

app_name = 'api-orders'

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'order-status', OrderStatusViewSet, basename='order-status')
router.register(r'order-payments', OrderPaymentViewSet, basename='order-payment')
router.register(r'order-tracking', OrderTrackingViewSet, basename='order-tracking')

urlpatterns = [
    path('', include(router.urls)),
] 