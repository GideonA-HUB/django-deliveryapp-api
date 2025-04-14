from django.shortcuts import render
from rest_framework import generics, permissions, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Category, Service, ServiceOption, Tag,
    BusinessLocation, BusinessSchedule, ServiceRating, ServiceAvailability
)
from .serializers import (
    CategorySerializer, ServiceSerializer, ServiceOptionSerializer,
    TagSerializer, BusinessLocationSerializer, BusinessScheduleSerializer,
    ServiceSearchSerializer, ServiceFilterSerializer, ServiceRatingSerializer,
    ServiceAvailabilitySerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Avg
from geopy.distance import geodesic
import json
from rest_framework.decorators import action
from django.http import JsonResponse

# Create your views here.

def test_api_view(request):
    return JsonResponse({"message": "API endpoint is working"})

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ServiceListView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'rating', 'created_at']

    def get_queryset(self):
        return Service.objects.filter(business=self.request.user.business_profile)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business_profile)

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(business=self.request.user.business_profile)

class ServiceOptionView(generics.ListCreateAPIView):
    serializer_class = ServiceOptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceOption.objects.filter(service__business=self.request.user.business_profile)

    def perform_create(self, serializer):
        service_id = self.kwargs.get('service_id')
        service = Service.objects.get(id=service_id, business=self.request.user.business_profile)
        serializer.save(service=service)

class ServiceSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ServiceSearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data.get('query', '')
            category = serializer.validated_data.get('category')
            min_price = serializer.validated_data.get('min_price')
            max_price = serializer.validated_data.get('max_price')
            tags = serializer.validated_data.get('tags', [])
            location = serializer.validated_data.get('location')
            radius = serializer.validated_data.get('radius')
            sort_by = serializer.validated_data.get('sort_by')
            order = serializer.validated_data.get('order', 'desc')

            queryset = Service.objects.filter(is_available=True)

            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
                )

            if category:
                queryset = queryset.filter(category__name=category)

            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)

            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)

            if tags:
                queryset = queryset.filter(tags__name__in=tags).distinct()

            if location and radius:
                # Implement location-based filtering
                pass

            if sort_by:
                if order == 'desc':
                    sort_by = f'-{sort_by}'
                queryset = queryset.order_by(sort_by)

            serializer = ServiceSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class BusinessLocationView(generics.ListCreateAPIView):
    serializer_class = BusinessLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessLocation.objects.filter(business=self.request.user.business_profile)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business_profile)

class BusinessScheduleView(generics.ListCreateAPIView):
    serializer_class = BusinessScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessSchedule.objects.filter(business=self.request.user.business_profile)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business_profile)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        services = Service.objects.filter(name__icontains=query)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

class ServiceOptionViewSet(viewsets.ModelViewSet):
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceOption.objects.filter(service__business=self.request.user.business_profile)

    def perform_create(self, serializer):
        service_id = self.request.data.get('service')
        service = Service.objects.get(id=service_id, business=self.request.user.business_profile)
        serializer.save(service=service)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(services__business=self.request.user.business_profile).distinct()

    def perform_create(self, serializer):
        serializer.save()

class BusinessLocationViewSet(viewsets.ModelViewSet):
    queryset = BusinessLocation.objects.all()
    serializer_class = BusinessLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessLocation.objects.filter(business=self.request.user.business_profile)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business_profile)

class BusinessScheduleViewSet(viewsets.ModelViewSet):
    queryset = BusinessSchedule.objects.all()
    serializer_class = BusinessScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessSchedule.objects.filter(business=self.request.user.business_profile)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business_profile)

def services_api_view(request):
    return render(request, 'api/services.html')

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'is_active']
    search_fields = ['name', 'description']

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        category = self.get_object()
        services = Service.objects.filter(category=category, is_available=True)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

class ServiceRatingViewSet(viewsets.ModelViewSet):
    queryset = ServiceRating.objects.all()
    serializer_class = ServiceRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service', 'rating', 'customer']

    def get_queryset(self):
        return ServiceRating.objects.filter(service__business=self.request.user.business_profile)

    def perform_create(self, serializer):
        service_id = self.request.data.get('service')
        service = Service.objects.get(id=service_id, business=self.request.user.business_profile)
        serializer.save(service=service, customer=self.request.user.customer_profile)

    @action(detail=False, methods=['get'])
    def average_rating(self, request):
        service_id = request.query_params.get('service')
        if service_id:
            average = ServiceRating.objects.filter(service_id=service_id).aggregate(Avg('rating'))
            return Response({'average_rating': average['rating__avg']})
        return Response({'error': 'Service ID is required'}, status=400)

class ServiceAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceAvailability.objects.filter(service__business=self.request.user.business_profile)

    def perform_create(self, serializer):
        service_id = self.request.data.get('service')
        service = Service.objects.get(id=service_id, business=self.request.user.business_profile)
        serializer.save(service=service)

    @action(detail=False, methods=['get'])
    def check_availability(self, request):
        service_id = request.query_params.get('service')
        date = request.query_params.get('date')
        if service_id and date:
            availability = ServiceAvailability.objects.filter(
                service_id=service_id,
                date=date,
                is_available=True
            ).first()
            if availability:
                return Response({'is_available': True, 'slots': availability.available_slots})
            return Response({'is_available': False})
        return Response({'error': 'Service ID and date are required'}, status=400)
