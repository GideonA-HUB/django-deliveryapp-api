from rest_framework import serializers
from .models import (
    Cart, CartItem, Order, OrderItem,
    OrderTracking, OrderStatus, OrderPayment
)
from services.serializers import ServiceSerializer, ServiceOptionSerializer
from accounts.serializers import UserSerializer, CustomerProfileSerializer
from services.models import Service, ServiceOption

class CartItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    selected_options = ServiceOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('cart', 'created_at', 'updated_at')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('customer', 'created_at', 'updated_at')
    
    def get_total(self, obj):
        return sum(item.service.price * item.quantity for item in obj.items.all())

class OrderItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    selected_options = ServiceOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('order', 'price')

class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = '__all__'
        read_only_fields = ('order', 'created_at')

class OrderStatusSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = OrderStatus
        fields = ['id', 'order', 'status', 'notes', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('amount') <= 0:
            raise serializers.ValidationError("Payment amount must be greater than zero")
        return data

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    status_updates = OrderStatusSerializer(many=True, read_only=True)
    payments = OrderPaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'items', 'status',
            'status_updates', 'payment_status', 'total_amount',
            'created_at', 'updated_at', 'payments'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    delivery_address = serializers.CharField()
    delivery_instructions = serializers.CharField(required=False)
    payment_method = serializers.ChoiceField(choices=OrderPayment.PAYMENT_METHOD_CHOICES)

class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS_CHOICES)
    notes = serializers.CharField(required=False)

class OrderTrackingUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS_CHOICES)
    location = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)

class CartItemCreateSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    selected_options = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    special_instructions = serializers.CharField(required=False)

class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    selected_options = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    special_instructions = serializers.CharField(required=False)

class OrderItemCreateSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ServiceOption.objects.all(),
        required=False
    )

    class Meta:
        model = OrderItem
        fields = [
            'service', 'quantity', 'price',
            'special_instructions', 'selected_options'
        ]

    def validate(self, data):
        service = data.get('service')
        quantity = data.get('quantity', 1)
        
        if quantity < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        
        if service and not service.is_available:
            raise serializers.ValidationError("Service is not available")
        
        # Validate selected options belong to the service
        selected_options = data.get('selected_options', [])
        if selected_options:
            for option in selected_options:
                if option.service != service:
                    raise serializers.ValidationError(
                        f"Option {option.name} does not belong to service {service.name}"
                    )
        
        return data

    def create(self, validated_data):
        selected_options = validated_data.pop('selected_options', [])
        order_item = OrderItem.objects.create(**validated_data)
        order_item.selected_options.set(selected_options)
        return order_item 