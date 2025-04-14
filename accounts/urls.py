from django.urls import path
from .views import (
    UserRegistrationView, BusinessRegistrationView, RiderRegistrationView,
    UserLoginView, UserLogoutView, UserProfileView, BusinessProfileView,
    CustomerProfileView, RiderProfileView
)

urlpatterns = [
    # Registration endpoints
    path('register/user/', UserRegistrationView.as_view(), name='user-register'),
    path('register/business/', BusinessRegistrationView.as_view(), name='business-register'),
    path('register/rider/', RiderRegistrationView.as_view(), name='rider-register'),
    
    # Authentication endpoints
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    
    # Profile endpoints
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/business/', BusinessProfileView.as_view(), name='business-profile'),
    path('profile/customer/', CustomerProfileView.as_view(), name='customer-profile'),
    path('profile/rider/', RiderProfileView.as_view(), name='rider-profile'),
] 