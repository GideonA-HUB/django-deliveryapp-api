from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartView, CartItemView, CartItemDetailView,
    OrderListView, OrderCreateView, OrderDetailView,
    OrderStatusUpdateView, OrderPaymentView,
    OrderViewSet, OrderItemViewSet, OrderStatusViewSet,
    OrderItemCreateView, orders_api_view
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'order-statuses', OrderStatusViewSet, basename='order-status')

app_name = 'orders'

urlpatterns = [
    # API ViewSet routes
    path('', include(router.urls)),
    
    # Template-based routes
    path('web/', orders_api_view, name='orders-web'),
    
    # Cart endpoints
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/items/', CartItemView.as_view(), name='cart-item-list'),
    path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    
    # Order endpoints
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('orders/<int:pk>/payment/', OrderPaymentView.as_view(), name='order-payment'),
    path('orders/<int:order_id>/items/create/', OrderItemCreateView.as_view(), name='order-item-create'),
] 