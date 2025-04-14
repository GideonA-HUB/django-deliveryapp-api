from django.urls import path
from .views import (
    ServiceRecommendationsView,
    UserRecommendationsView,
    PopularServicesView,
    SimilarServicesView
)

urlpatterns = [
    # Get service recommendations
    path('services/', ServiceRecommendationsView.as_view(), name='service-recommendations'),
    
    # Get user-specific recommendations
    path('user/', UserRecommendationsView.as_view(), name='user-recommendations'),
    
    # Get popular services
    path('popular/', PopularServicesView.as_view(), name='popular-services'),
    
    # Get similar services
    path('similar/<int:service_id>/', SimilarServicesView.as_view(), name='similar-services'),
] 