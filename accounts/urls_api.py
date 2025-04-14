from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserListView,
    UserDetailView,
    CustomerProfileView,
    BusinessProfileView,
    RiderProfileView,
)

app_name = 'api-auth'

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Management
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Profile Management
    path('customer/profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('business/profile/', BusinessProfileView.as_view(), name='business-profile'),
    path('rider/profile/', RiderProfileView.as_view(), name='rider-profile'),
] 