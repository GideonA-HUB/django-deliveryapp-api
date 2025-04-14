from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import CustomerProfile, BusinessProfile, RiderProfile
from services.models import Service, ServiceOption, Category
from orders.models import Order, OrderItem, OrderStatus

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up test data for the application'

    def handle(self, *args, **kwargs):
        # Get or create test users
        customer_user, _ = User.objects.get_or_create(
            username='test_customer',
            defaults={
                'email': 'customer@test.com',
                'password': 'testpass123',
                'user_type': 'customer',
                'phone_number': '1234567890'
            }
        )
        customer_user.set_password('testpass123')
        customer_user.save()
        
        business_user, _ = User.objects.get_or_create(
            username='test_business',
            defaults={
                'email': 'business@test.com',
                'password': 'testpass123',
                'user_type': 'business',
                'phone_number': '1234567890'
            }
        )
        business_user.set_password('testpass123')
        business_user.save()
        
        rider_user, _ = User.objects.get_or_create(
            username='test_rider',
            defaults={
                'email': 'rider@test.com',
                'password': 'testpass123',
                'user_type': 'rider',
                'phone_number': '1234567890'
            }
        )
        rider_user.set_password('testpass123')
        rider_user.save()

        # Get or create profiles
        customer_profile, _ = CustomerProfile.objects.get_or_create(
            user=customer_user,
            defaults={'address': '123 Customer St'}
        )
        
        business_profile, _ = BusinessProfile.objects.get_or_create(
            user=business_user,
            defaults={
                'business_name': 'Test Business',
                'business_type': 'restaurant',
                'description': 'A test business'
            }
        )
        
        rider_profile, _ = RiderProfile.objects.get_or_create(
            user=rider_user,
            defaults={
                'vehicle_type': 'bicycle',
                'license_number': 'TEST123'
            }
        )

        # Create a test category
        category, _ = Category.objects.get_or_create(
            name='Test Category',
            defaults={
                'description': 'A test category',
                'icon': 'fa-utensils'
            }
        )

        # Create a test service
        service, _ = Service.objects.get_or_create(
            business=business_profile,
            name='Test Service',
            defaults={
                'category': category,
                'description': 'A test service',
                'price': 10.00,
                'is_available': True,
                'preparation_time': 30
            }
        )

        # Create a test order
        order, _ = Order.objects.get_or_create(
            order_number='TEST001',
            defaults={
                'customer': customer_profile,
                'business': business_profile,
                'rider': rider_profile,
                'status': 'pending',
                'payment_status': 'pending',
                'total_amount': 20.00,
                'delivery_address': '123 Test St',
                'delivery_instructions': 'Test instructions'
            }
        )

        # Create order items
        OrderItem.objects.get_or_create(
            order=order,
            service=service,
            defaults={
                'quantity': 2,
                'price': 10.00
            }
        )

        # Create initial order status
        OrderStatus.objects.get_or_create(
            order=order,
            status='pending',
            defaults={
                'notes': 'Order created',
                'created_by': customer_user
            }
        )

        self.stdout.write(self.style.SUCCESS('Test data created/updated successfully!')) 