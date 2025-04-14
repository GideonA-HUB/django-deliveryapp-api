from django.urls import path
from .views import (
    UserLoginView, UserLogoutView, UserRegistrationView,
    UserProfileView, UserPasswordChangeView, UserPasswordResetView,
    UserPasswordResetConfirmView, UserActivationView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('activate/<uidb64>/<token>/', UserActivationView.as_view(), name='activate'),
] 