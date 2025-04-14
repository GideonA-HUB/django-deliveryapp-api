from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Cart, CartItem, Order, OrderItem,
    OrderTracking, OrderStatus, OrderPayment
)
from .serializers import (
    CartSerializer, CartItemSerializer,
    OrderSerializer, OrderCreateSerializer,
    OrderStatusUpdateSerializer, OrderPaymentSerializer,
    OrderTrackingUpdateSerializer, CartItemCreateSerializer,
    CartItemUpdateSerializer, OrderItemSerializer, OrderStatusSerializer,
    OrderItemCreateSerializer, OrderTrackingSerializer
)
from services.models import Service, ServiceOption
import random
import string
from accounts.models import CustomerProfile
from rest_framework.decorators import action
from django.db.models import Q, Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse

def orders_api_view(request):
    return render(request, 'api/orders.html')

def test_api_view(request):
    return JsonResponse({"message": "API endpoint is working"})

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(customer=self.request.user.customer_profile)
        return cart

class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = get_object_or_404(Cart, customer=self.request.user.customer_profile)
        return CartItem.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        serializer = CartItemCreateSerializer(data=request.data)
        if serializer.is_valid():
            cart = get_object_or_404(Cart, customer=request.user.customer_profile)
            service = get_object_or_404(Service, id=serializer.validated_data['service_id'])
            
            selected_options = []
            if 'selected_options' in serializer.validated_data:
                selected_options = ServiceOption.objects.filter(
                    id__in=serializer.validated_data['selected_options'],
                    service=service
                )
            
            cart_item = CartItem.objects.create(
                cart=cart,
                service=service,
                quantity=serializer.validated_data['quantity'],
                special_instructions=serializer.validated_data.get('special_instructions', '')
            )
            cart_item.selected_options.set(selected_options)
            
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = get_object_or_404(Cart, customer=self.request.user.customer_profile)
        return CartItem.objects.filter(cart=cart)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'customer':
            return Order.objects.filter(customer=self.request.user.customer_profile)
        elif self.request.user.user_type == 'business':
            return Order.objects.filter(business=self.request.user.business_profile)
        elif self.request.user.user_type == 'rider':
            return Order.objects.filter(rider=self.request.user.rider_profile)
        return Order.objects.none()

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            cart = get_object_or_404(Cart, id=serializer.validated_data['cart_id'])
            
            # Generate order number
            order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            # Create order
            order = Order.objects.create(
                customer=request.user.customer_profile,
                business=cart.items.first().service.business,
                order_number=order_number,
                delivery_address=serializer.validated_data['delivery_address'],
                delivery_instructions=serializer.validated_data.get('delivery_instructions', ''),
                total_amount=sum(item.service.price * item.quantity for item in cart.items.all())
            )
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    service=cart_item.service,
                    quantity=cart_item.quantity,
                    price=cart_item.service.price,
                    special_instructions=cart_item.special_instructions
                )
                cart_item.selected_options.set(cart_item.selected_options.all())
            
            # Create initial tracking
            OrderTracking.objects.create(
                order=order,
                status='pending'
            )
            
            # Clear cart
            cart.items.all().delete()
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'customer':
            return Order.objects.filter(customer=self.request.user.customer_profile)
        elif self.request.user.user_type == 'business':
            return Order.objects.filter(business=self.request.user.business_profile)
        elif self.request.user.user_type == 'rider':
            return Order.objects.filter(rider=self.request.user.rider_profile)
        return Order.objects.none()

class OrderStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderStatusUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            status = serializer.validated_data['status']
            notes = serializer.validated_data.get('notes', '')
            
            # Update order status
            order.status = status
            order.save()
            
            # Create tracking update
            OrderTracking.objects.create(
                order=order,
                status=status,
                notes=notes
            )
            
            return Response(OrderSerializer(order).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, customer=request.user.customer_profile)
        serializer = OrderPaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = OrderPayment.objects.create(
                order=order,
                amount=order.total_amount,
                payment_method=serializer.validated_data['payment_method'],
                status='pending'
            )
            # Update order payment status
            order.payment_status = 'paid'
            order.save()
            return Response(OrderPaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'customer':
            customer_profile = CustomerProfile.objects.get(user=self.request.user)
            return Order.objects.filter(customer=customer_profile)
        elif self.request.user.user_type == 'business':
            return Order.objects.filter(business__user=self.request.user)
        elif self.request.user.user_type == 'rider':
            return Order.objects.filter(rider__user=self.request.user)
        return Order.objects.none()

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')

        if not new_status:
            return Response(
                {'error': 'Status is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in dict(Order.ORDER_STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        OrderStatus.objects.create(
            order=order,
            status=new_status,
            notes=notes,
            created_by=request.user
        )
        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('order_pk')
        return OrderItem.objects.filter(order_id=order_id)

class OrderStatusViewSet(viewsets.ModelViewSet):
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('order_pk')
        return OrderStatus.objects.filter(order_id=order_id)

class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id, customer=self.request.user.customer_profile)
        serializer.save(order=order)

class OrderPaymentViewSet(viewsets.ModelViewSet):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'status', 'payment_method']

    def get_queryset(self):
        return OrderPayment.objects.filter(order__customer=self.request.user.customer_profile)

    def perform_create(self, serializer):
        order_id = self.request.data.get('order')
        order = Order.objects.get(id=order_id, customer=self.request.user.customer_profile)
        serializer.save(order=order)

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        payment = self.get_object()
        # Add payment processing logic here
        payment.status = 'completed'
        payment.save()
        return Response({'status': 'Payment processed successfully'})

class OrderTrackingViewSet(viewsets.ModelViewSet):
    queryset = OrderTracking.objects.all()
    serializer_class = OrderTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'status']

    def get_queryset(self):
        return OrderTracking.objects.filter(order__customer=self.request.user.customer_profile)

    def perform_create(self, serializer):
        order_id = self.request.data.get('order')
        order = Order.objects.get(id=order_id, customer=self.request.user.customer_profile)
        serializer.save(order=order)

    @action(detail=True, methods=['get'])
    def current_status(self, request, pk=None):
        tracking = self.get_object()
        return Response({
            'status': tracking.status,
            'location': tracking.location,
            'updated_at': tracking.updated_at
        })
