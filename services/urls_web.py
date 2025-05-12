from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceViewSet.as_view({'get': 'list'}), name='service_list'),
    path('<int:pk>/', views.ServiceViewSet.as_view({'get': 'retrieve'}), name='service_detail'),
    path('categories/', views.ServiceCategoryViewSet.as_view({'get': 'list'}), name='category_list'),
    path('categories/<int:pk>/', views.ServiceCategoryViewSet.as_view({'get': 'retrieve'}), name='category_detail'),
    path('ratings/', views.ServiceRatingViewSet.as_view({'get': 'list'}), name='rating_list'),
    path('availability/', views.ServiceAvailabilityViewSet.as_view({'get': 'list'}), name='availability_list'),
    path('web/', views.test_api_view, name='test_api'),
    path('register/', views.customer_register, name='customer_register'),
]