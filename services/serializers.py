from rest_framework import serializers
from .models import (
    Category, Service, ServiceOption, Tag,
    BusinessLocation, BusinessSchedule, ServiceRating, ServiceAvailability
)
from accounts.serializers import CustomerProfileSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOption
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    options = ServiceOptionSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('business', 'created_at', 'updated_at')

class CategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')

class BusinessLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessLocation
        fields = ['id', 'business', 'address', 'latitude', 'longitude', 'is_primary', 'created_at', 'updated_at']
        read_only_fields = ('business', 'created_at', 'updated_at')

class BusinessScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessSchedule
        fields = ['id', 'business', 'day', 'opening_time', 'closing_time', 'is_closed']
        read_only_fields = ('business',)

class ServiceSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    location = serializers.CharField(required=False)
    radius = serializers.FloatField(required=False)
    sort_by = serializers.ChoiceField(
        choices=['price', 'rating', 'distance', 'popularity'],
        required=False
    )
    order = serializers.ChoiceField(
        choices=['asc', 'desc'],
        required=False
    )

class ServiceFilterSerializer(serializers.Serializer):
    category = serializers.CharField(required=False)
    price_range = serializers.ListField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2),
        required=False
    )
    rating = serializers.FloatField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    is_available = serializers.BooleanField(required=False)
    preparation_time = serializers.IntegerField(required=False)

class ServiceRatingSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(read_only=True)
    
    class Meta:
        model = ServiceRating
        fields = ['id', 'service', 'customer', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['customer', 'created_at', 'updated_at']

class ServiceAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAvailability
        fields = ['id', 'service', 'date', 'start_time', 'end_time', 'is_available', 'available_slots', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 