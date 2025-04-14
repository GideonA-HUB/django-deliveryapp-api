from django.urls import path
from delivery.views_web import DeliveryListView, DeliveryDetailView
from delivery.views import DeliveryTrackingViewSet, DeliveryZoneListCreateView, DeliveryFeeListCreateView
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', DeliveryListView.as_view(), name='delivery_list'),
    path('<int:pk>/', DeliveryDetailView.as_view(), name='delivery_detail'),
    path('assignments/', views.DeliveryAssignmentListView.as_view(), name='assignment_list'),
    path('tracking/', DeliveryTrackingViewSet.as_view({'get': 'list'}), name='tracking_list'),
    path('zones/', DeliveryZoneListCreateView.as_view(), name='zone_list'),
    path('fees/', DeliveryFeeListCreateView.as_view(), name='fee_list'),
    path('web/', views.test_api_view, name='test_api'),
]