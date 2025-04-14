from django.shortcuts import render
from django.db.models import Count, Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.models import Service
from orders.models import Order, OrderItem
from services.serializers import ServiceSerializer

# Create your views here.

class ServiceRecommendationsView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get user's order history
        ordered_services = OrderItem.objects.filter(
            order__user=user
        ).values_list('service', flat=True)

        # Get services similar to what user has ordered
        similar_services = Service.objects.filter(
            category__in=Service.objects.filter(id__in=ordered_services).values('category')
        ).exclude(id__in=ordered_services)

        return similar_services[:10]

class UserRecommendationsView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get user's location
        user_location = user.location if hasattr(user, 'location') else None

        if user_location:
            # Get services near user's location
            nearby_services = Service.objects.filter(
                business__location__distance_lte=(user_location, 10000)  # Within 10km
            )
            return nearby_services.order_by('business__location__distance')[:10]
        
        # Fallback to popular services if location not available
        return Service.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:10]

class PopularServicesView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get most ordered services in the last 30 days
        return Service.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:10]

class SimilarServicesView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        service = Service.objects.get(id=service_id)

        # Get services in the same category with similar price range
        similar_services = Service.objects.filter(
            Q(category=service.category) &
            Q(price__range=(service.price * 0.8, service.price * 1.2))  # Within 20% price range
        ).exclude(id=service_id)

        return similar_services[:10]
