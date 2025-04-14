"""
URL configuration for delivery_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Delivery Service API",
      default_version='v1',
      description="API documentation for the Delivery Service platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@deliveryservice.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('accounts.urls_api', namespace='api-auth')),
    path('api/services/', include('services.urls_api', namespace='api-services')),
    path('api/orders/', include('orders.urls_api', namespace='api-orders')),
    path('api/delivery/', include('delivery.urls_api', namespace='api-delivery')),
    path('api/notifications/', include('notifications.urls_api', namespace='api-notifications')),
    path('api/chat/', include('chat.urls_api', namespace='api-chat')),
    
    # Template-based routes
    path('', include('accounts.urls_web', namespace='web-auth')),
    path('services/', include('services.urls_web', namespace='web-services')),
    path('orders/', include('orders.urls_web', namespace='web-orders')),
    path('delivery/', include('delivery.urls_web', namespace='web-delivery')),
    path('notifications/', include('notifications.urls_web', namespace='web-notifications')),
    path('chat/', include('chat.urls_web', namespace='web-chat')),
    
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.logout_view, name='logout'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('business/dashboard/', views.business_dashboard, name='business_dashboard'),
    path('rider/dashboard/', views.rider_dashboard, name='rider_dashboard'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
