from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderViewSet.as_view({'get': 'list'}), name='order_list'),
    path('<int:pk>/', views.OrderViewSet.as_view({'get': 'retrieve'}), name='order_detail'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/cancel/', views.OrderViewSet.as_view({'post': 'cancel'}), name='order_cancel'),
    path('payment/', views.OrderPaymentViewSet.as_view({'get': 'list'}), name='payment_list'),
    path('web/', views.test_api_view, name='test_api'),
]