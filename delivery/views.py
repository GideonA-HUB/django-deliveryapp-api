from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import (
    DeliveryAssignment, DeliveryLocation,
    DeliveryRating, DeliveryZone,
    ZoneBoundary, DeliveryFee, Delivery, DeliveryTracking
)
from .serializers import (
    DeliveryAssignmentSerializer, DeliveryLocationSerializer,
    DeliveryRatingSerializer, DeliveryZoneSerializer,
    DeliveryFeeSerializer, DeliveryAssignmentCreateSerializer,
    DeliveryLocationUpdateSerializer, DeliveryStatusUpdateSerializer,
    DeliveryRatingCreateSerializer, DeliveryZoneCreateSerializer,
    DeliveryFeeCreateSerializer, DeliverySerializer, DeliveryTrackingSerializer,
    ZoneBoundarySerializer
)
from orders.models import Order
from accounts.models import RiderProfile
from rest_framework.decorators import action
from django.http import JsonResponse

class DeliveryAssignmentListView(generics.ListAPIView):
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'rider':
            return DeliveryAssignment.objects.filter(rider=self.request.user.rider_profile)
        elif self.request.user.user_type == 'business':
            return DeliveryAssignment.objects.filter(order__business=self.request.user.business_profile)
        return DeliveryAssignment.objects.none()

class DeliveryAssignmentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DeliveryAssignmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = get_object_or_404(Order, id=serializer.validated_data['order_id'])
            rider = get_object_or_404(RiderProfile, id=serializer.validated_data['rider_id'])
            
            assignment = DeliveryAssignment.objects.create(
                order=order,
                rider=rider,
                status='assigned',
                notes=serializer.validated_data.get('notes', '')
            )
            
            # Update order status
            order.status = 'assigned'
            order.rider = rider
            order.save()
            
            return Response(DeliveryAssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryAssignmentDetailView(generics.RetrieveAPIView):
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'rider':
            return DeliveryAssignment.objects.filter(rider=self.request.user.rider_profile)
        elif self.request.user.user_type == 'business':
            return DeliveryAssignment.objects.filter(order__business=self.request.user.business_profile)
        return DeliveryAssignment.objects.none()

class DeliveryStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        assignment = get_object_or_404(DeliveryAssignment, pk=pk)
        serializer = DeliveryStatusUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            status = serializer.validated_data['status']
            location_data = serializer.validated_data.get('location')
            notes = serializer.validated_data.get('notes', '')
            
            # Update assignment status
            assignment.status = status
            if status == 'picked_up':
                assignment.picked_up_at = timezone.now()
            elif status == 'delivered':
                assignment.delivered_at = timezone.now()
            assignment.save()
            
            # Update order status
            assignment.order.status = status
            assignment.order.save()
            
            # Create location update if provided
            if location_data:
                DeliveryLocation.objects.create(
                    assignment=assignment,
                    **location_data
                )
            
            return Response(DeliveryAssignmentSerializer(assignment).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryLocationUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        assignment = get_object_or_404(DeliveryAssignment, pk=pk)
        serializer = DeliveryLocationUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            location = DeliveryLocation.objects.create(
                assignment=assignment,
                **serializer.validated_data
            )
            return Response(DeliveryLocationSerializer(location).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryRatingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        assignment = get_object_or_404(DeliveryAssignment, pk=pk)
        serializer = DeliveryRatingCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            rating = DeliveryRating.objects.create(
                assignment=assignment,
                **serializer.validated_data
            )
            
            # Update rider rating
            rider_ratings = DeliveryRating.objects.filter(assignment__rider=assignment.rider)
            avg_rating = sum(r.rating for r in rider_ratings) / rider_ratings.count()
            assignment.rider.rating = avg_rating
            assignment.rider.save()
            
            return Response(DeliveryRatingSerializer(rating).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryZoneListCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryZoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeliveryZone.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DeliveryZoneCreateSerializer(data=request.data)
        if serializer.is_valid():
            zone = DeliveryZone.objects.create(
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', '')
            )
            
            # Create boundaries
            boundaries = []
            for i, boundary_data in enumerate(serializer.validated_data['boundaries']):
                boundaries.append(ZoneBoundary(
                    zone=zone,
                    latitude=boundary_data['latitude'],
                    longitude=boundary_data['longitude'],
                    order=i
                ))
            ZoneBoundary.objects.bulk_create(boundaries)
            
            return Response(DeliveryZoneSerializer(zone).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryFeeListCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryFeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeliveryFee.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DeliveryFeeCreateSerializer(data=request.data)
        if serializer.is_valid():
            zone = get_object_or_404(DeliveryZone, id=serializer.validated_data['zone_id'])
            fee = DeliveryFee.objects.create(
                zone=zone,
                min_distance=serializer.validated_data['min_distance'],
                max_distance=serializer.validated_data['max_distance'],
                fee=serializer.validated_data['fee']
            )
            return Response(DeliveryFeeSerializer(fee).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryAssignmentViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAssignment.objects.all()
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryZoneViewSet(viewsets.ModelViewSet):
    queryset = DeliveryZone.objects.all()
    serializer_class = DeliveryZoneSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryFeeViewSet(viewsets.ModelViewSet):
    queryset = DeliveryFee.objects.all()
    serializer_class = DeliveryFeeSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryRatingViewSet(viewsets.ModelViewSet):
    queryset = DeliveryRating.objects.all()
    serializer_class = DeliveryRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'rider':
            return Delivery.objects.filter(rider=self.request.user.rider_profile)
        elif self.request.user.user_type == 'business':
            return Delivery.objects.filter(order__business=self.request.user.business_profile)
        return Delivery.objects.none()

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        delivery = self.get_object()
        serializer = DeliveryStatusUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            status = serializer.validated_data['status']
            location_data = serializer.validated_data.get('location')
            notes = serializer.validated_data.get('notes', '')
            
            # Update delivery status
            delivery.status = status
            if status == 'picked_up':
                delivery.picked_up_at = timezone.now()
            elif status == 'delivered':
                delivery.delivered_at = timezone.now()
            delivery.save()
            
            # Update order status
            delivery.order.status = status
            delivery.order.save()
            
            # Create location update if provided
            if location_data:
                DeliveryLocation.objects.create(
                    delivery=delivery,
                    **location_data
                )
            
            return Response(DeliverySerializer(delivery).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryTrackingViewSet(viewsets.ModelViewSet):
    queryset = DeliveryTracking.objects.all()
    serializer_class = DeliveryTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'rider':
            return DeliveryTracking.objects.filter(delivery__rider=self.request.user.rider_profile)
        elif self.request.user.user_type == 'business':
            return DeliveryTracking.objects.filter(delivery__order__business=self.request.user.business_profile)
        return DeliveryTracking.objects.none()

    @action(detail=True, methods=['get'])
    def current_location(self, request, pk=None):
        tracking = self.get_object()
        return Response({
            'latitude': tracking.latitude,
            'longitude': tracking.longitude,
            'updated_at': tracking.updated_at
        })

class DeliveryLocationViewSet(viewsets.ModelViewSet):
    queryset = DeliveryLocation.objects.all()
    serializer_class = DeliveryLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'rider':
            return DeliveryLocation.objects.filter(assignment__rider=self.request.user.rider_profile)
        elif self.request.user.user_type == 'business':
            return DeliveryLocation.objects.filter(assignment__order__business=self.request.user.business_profile)
        return DeliveryLocation.objects.none()

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        location = self.get_object()
        serializer = DeliveryLocationUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            location.latitude = serializer.validated_data['latitude']
            location.longitude = serializer.validated_data['longitude']
            location.speed = serializer.validated_data.get('speed')
            location.accuracy = serializer.validated_data.get('accuracy')
            location.save()
            
            return Response(DeliveryLocationSerializer(location).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ZoneBoundaryViewSet(viewsets.ModelViewSet):
    queryset = ZoneBoundary.objects.all()
    serializer_class = ZoneBoundarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        zone_id = self.request.query_params.get('zone_id')
        if zone_id:
            return ZoneBoundary.objects.filter(zone_id=zone_id).order_by('order')
        return ZoneBoundary.objects.none()

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        zone_id = request.data.get('zone_id')
        boundaries = request.data.get('boundaries', [])
        
        if not zone_id or not boundaries:
            return Response(
                {'error': 'zone_id and boundaries are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        zone = get_object_or_404(DeliveryZone, id=zone_id)
        
        # Delete existing boundaries
        ZoneBoundary.objects.filter(zone=zone).delete()
        
        # Create new boundaries
        new_boundaries = []
        for i, boundary_data in enumerate(boundaries):
            new_boundaries.append(ZoneBoundary(
                zone=zone,
                latitude=boundary_data['latitude'],
                longitude=boundary_data['longitude'],
                order=i
            ))
        
        ZoneBoundary.objects.bulk_create(new_boundaries)
        
        return Response(
            ZoneBoundarySerializer(ZoneBoundary.objects.filter(zone=zone), many=True).data,
            status=status.HTTP_201_CREATED
        )

def delivery_api_view(request):
    return render(request, 'api/delivery.html')

def test_api_view(request):
    return JsonResponse({"message": "API endpoint is working"})
