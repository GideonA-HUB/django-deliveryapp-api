from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView, CategoryDetailView,
    ServiceListView, ServiceDetailView,
    ServiceOptionView, ServiceSearchView,
    BusinessLocationView, BusinessScheduleView,
    CategoryViewSet, ServiceViewSet,
    ServiceOptionViewSet, TagViewSet,
    BusinessLocationViewSet, BusinessScheduleViewSet,
    services_api_view
)
from .views_web import ServiceListView as WebServiceListView, ServiceDetailView as WebServiceDetailView

app_name = 'services'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'options', ServiceOptionViewSet)
router.register(r'tags', TagViewSet)
router.register(r'locations', BusinessLocationViewSet)
router.register(r'schedules', BusinessScheduleViewSet)

urlpatterns = [
    # API ViewSet routes
    path('', include(router.urls)),
    
    # Template-based routes
    path('web/', WebServiceListView.as_view(), name='services-web'),
    path('web/<int:pk>/', WebServiceDetailView.as_view(), name='service-detail'),
    
    # Original API endpoints
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:service_id>/options/', ServiceOptionView.as_view(), name='service-option-list'),
    path('search/', ServiceSearchView.as_view(), name='service-search'),
    path('locations/', BusinessLocationView.as_view(), name='business-location-list'),
    path('schedules/', BusinessScheduleView.as_view(), name='business-schedule-list'),
] 