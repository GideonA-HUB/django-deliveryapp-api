from django.urls import path
from .views import (
    AnalyticsDashboardView,
    OrderAnalyticsView,
    RevenueAnalyticsView,
    UserAnalyticsView,
    ServiceAnalyticsView
)

urlpatterns = [
    # Analytics dashboard
    path('dashboard/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    
    # Order analytics
    path('orders/', OrderAnalyticsView.as_view(), name='order-analytics'),
    
    # Revenue analytics
    path('revenue/', RevenueAnalyticsView.as_view(), name='revenue-analytics'),
    
    # User analytics
    path('users/', UserAnalyticsView.as_view(), name='user-analytics'),
    
    # Service analytics
    path('services/', ServiceAnalyticsView.as_view(), name='service-analytics'),
] 