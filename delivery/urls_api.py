from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeliveryViewSet,
    DeliveryAssignmentViewSet,
    DeliveryLocationViewSet,
    DeliveryZoneViewSet,
    DeliveryTrackingViewSet,
    DeliveryRatingViewSet,
    ZoneBoundaryViewSet,
    DeliveryFeeViewSet,
)

app_name = 'api-delivery'

router = DefaultRouter()
router.register(r'deliveries', DeliveryViewSet, basename='delivery')
router.register(r'assignments', DeliveryAssignmentViewSet, basename='assignment')
router.register(r'locations', DeliveryLocationViewSet, basename='location')
router.register(r'zones', DeliveryZoneViewSet, basename='zone')
router.register(r'tracking', DeliveryTrackingViewSet, basename='tracking')
router.register(r'ratings', DeliveryRatingViewSet, basename='rating')
router.register(r'boundaries', ZoneBoundaryViewSet, basename='boundary')
router.register(r'fees', DeliveryFeeViewSet, basename='fee')

urlpatterns = [
    path('', include(router.urls)),
] 