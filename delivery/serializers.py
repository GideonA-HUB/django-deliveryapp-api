from rest_framework import serializers
from .models import (
    DeliveryAssignment, DeliveryLocation,
    DeliveryRating, DeliveryZone,
    ZoneBoundary, DeliveryFee, Delivery, DeliveryTracking
)
from orders.serializers import OrderSerializer
from accounts.serializers import RiderProfileSerializer

class DeliveryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = '__all__'
        read_only_fields = ('assignment', 'timestamp')

class DeliveryRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRating
        fields = '__all__'
        read_only_fields = ('assignment', 'created_at')

class ZoneBoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneBoundary
        fields = ['id', 'zone', 'latitude', 'longitude', 'order']
        read_only_fields = ['id']

class DeliveryZoneSerializer(serializers.ModelSerializer):
    boundaries = ZoneBoundarySerializer(many=True, read_only=True)
    
    class Meta:
        model = DeliveryZone
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class DeliveryFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFee
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    rider = RiderProfileSerializer(read_only=True)
    order = OrderSerializer(read_only=True)
    locations = DeliveryLocationSerializer(many=True, read_only=True)
    ratings = DeliveryRatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = DeliveryAssignment
        fields = '__all__'
        read_only_fields = ('assigned_at', 'picked_up_at', 'delivered_at')

class DeliveryAssignmentCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    rider_id = serializers.IntegerField()
    notes = serializers.CharField(required=False)

class DeliveryLocationUpdateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    speed = serializers.FloatField(required=False)
    accuracy = serializers.FloatField(required=False)

class DeliveryStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered')
    ])
    location = DeliveryLocationUpdateSerializer(required=False)
    notes = serializers.CharField(required=False)

class DeliveryRatingCreateSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False)

class DeliveryZoneCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    boundaries = serializers.ListField(
        child=serializers.DictField(
            child=serializers.FloatField()
        )
    )

class DeliveryFeeCreateSerializer(serializers.Serializer):
    zone_id = serializers.IntegerField()
    min_distance = serializers.FloatField()
    max_distance = serializers.FloatField()
    fee = serializers.DecimalField(max_digits=10, decimal_places=2)

class DeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    rider = RiderProfileSerializer(read_only=True)
    locations = DeliveryLocationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'order', 'rider', 'status', 'picked_up_at',
            'delivered_at', 'notes', 'locations', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class DeliveryTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTracking
        fields = [
            'id', 'delivery', 'latitude', 'longitude',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ZoneBoundaryCreateSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    order = serializers.IntegerField(min_value=0) 