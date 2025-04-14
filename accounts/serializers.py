from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BusinessProfile, CustomerProfile, RiderProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'profile_picture')
        read_only_fields = ('id', 'user_type')

class BusinessProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        read_only_fields = ('user', 'rating', 'created_at', 'updated_at')

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class RiderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = RiderProfile
        fields = '__all__'
        read_only_fields = ('user', 'rating', 'created_at', 'updated_at')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'user_type', 'phone_number')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class BusinessRegistrationSerializer(UserRegistrationSerializer):
    business_data = serializers.JSONField(write_only=True)
    
    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + ('business_data',)
    
    def create(self, validated_data):
        business_data = validated_data.pop('business_data')
        user = super().create(validated_data)
        BusinessProfile.objects.create(user=user, **business_data)
        return user

class RiderRegistrationSerializer(UserRegistrationSerializer):
    rider_data = serializers.JSONField(write_only=True)
    
    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + ('rider_data',)
    
    def create(self, validated_data):
        rider_data = validated_data.pop('rider_data')
        user = super().create(validated_data)
        RiderProfile.objects.create(user=user, **rider_data)
        return user 