from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncDate
from orders.models import Order
from services.models import Service
from accounts.models import User

# Create your views here.

class AnalyticsDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Get date range (default: last 30 days)
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)

        # Order statistics
        orders = Order.objects.filter(created_at__range=[start_date, end_date])
        total_orders = orders.count()
        total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        average_order_value = orders.aggregate(Avg('total_amount'))['total_amount__avg'] or 0

        # User statistics
        total_users = User.objects.count()
        new_users = User.objects.filter(date_joined__range=[start_date, end_date]).count()

        return Response({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'average_order_value': average_order_value,
            'total_users': total_users,
            'new_users': new_users,
        })

class OrderAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Get date range (default: last 30 days)
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)

        # Daily order counts
        daily_orders = Order.objects.filter(
            created_at__range=[start_date, end_date]
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        # Order status distribution
        status_distribution = Order.objects.values('status').annotate(
            count=Count('id')
        )

        return Response({
            'daily_orders': daily_orders,
            'status_distribution': status_distribution,
        })

class RevenueAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Get date range (default: last 30 days)
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)

        # Daily revenue
        daily_revenue = Order.objects.filter(
            created_at__range=[start_date, end_date]
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            revenue=Sum('total_amount')
        ).order_by('date')

        return Response({
            'daily_revenue': daily_revenue,
        })

class UserAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Get date range (default: last 30 days)
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)

        # Daily new users
        daily_new_users = User.objects.filter(
            date_joined__range=[start_date, end_date]
        ).annotate(
            date=TruncDate('date_joined')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        # User type distribution
        user_types = {
            'customers': User.objects.filter(is_customer=True).count(),
            'businesses': User.objects.filter(is_business=True).count(),
            'riders': User.objects.filter(is_rider=True).count(),
        }

        return Response({
            'daily_new_users': daily_new_users,
            'user_types': user_types,
        })

class ServiceAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Get date range (default: last 30 days)
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)

        # Most ordered services
        top_services = Service.objects.filter(
            orderitem__order__created_at__range=[start_date, end_date]
        ).annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:10]

        # Service category distribution
        category_distribution = Service.objects.values('category').annotate(
            count=Count('id')
        )

        return Response({
            'top_services': top_services,
            'category_distribution': category_distribution,
        })
