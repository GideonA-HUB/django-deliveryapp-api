from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet,
    ServiceCategoryViewSet,
    ServiceOptionViewSet,
    ServiceRatingViewSet,
    ServiceAvailabilityViewSet,
)

app_name = 'api-services'

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'categories', ServiceCategoryViewSet, basename='category')
router.register(r'options', ServiceOptionViewSet, basename='option')
router.register(r'ratings', ServiceRatingViewSet, basename='rating')
router.register(r'availability', ServiceAvailabilityViewSet, basename='availability')

urlpatterns = [
    path('', include(router.urls)),
] 