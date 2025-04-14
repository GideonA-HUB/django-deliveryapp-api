from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeliveryAssignmentListView, DeliveryAssignmentCreateView,
    DeliveryAssignmentDetailView, DeliveryStatusUpdateView,
    DeliveryLocationUpdateView, DeliveryRatingCreateView,
    DeliveryZoneListCreateView, DeliveryFeeListCreateView,
    DeliveryAssignmentViewSet, DeliveryZoneViewSet,
    DeliveryFeeViewSet, DeliveryRatingViewSet,
    delivery_api_view
)

app_name = 'delivery'

router = DefaultRouter()
router.register(r'assignments', DeliveryAssignmentViewSet)
router.register(r'zones', DeliveryZoneViewSet)
router.register(r'fees', DeliveryFeeViewSet)
router.register(r'ratings', DeliveryRatingViewSet)

urlpatterns = [
    # API ViewSet routes
    path('', include(router.urls)),
    
    # Template-based routes
    path('web/', delivery_api_view, name='delivery-web'),
    
    # Original API endpoints
    path('assignments/', DeliveryAssignmentListView.as_view(), name='delivery-assignment-list'),
    path('assignments/create/', DeliveryAssignmentCreateView.as_view(), name='delivery-assignment-create'),
    path('assignments/<int:pk>/', DeliveryAssignmentDetailView.as_view(), name='delivery-assignment-detail'),
    path('assignments/<int:pk>/status/', DeliveryStatusUpdateView.as_view(), name='delivery-status-update'),
    path('assignments/<int:pk>/location/', DeliveryLocationUpdateView.as_view(), name='delivery-location-update'),
    path('assignments/<int:pk>/rating/', DeliveryRatingCreateView.as_view(), name='delivery-rating-create'),
    path('zones/', DeliveryZoneListCreateView.as_view(), name='delivery-zone-list'),
    path('fees/', DeliveryFeeListCreateView.as_view(), name='delivery-fee-list'),
] 