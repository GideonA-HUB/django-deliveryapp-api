from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from orders.models import Order
from accounts.models import CustomerProfile, CustomerAddress

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'customer':
            return redirect('customer_dashboard')
        elif request.user.user_type == 'business':
            return redirect('business_dashboard')
        elif request.user.user_type == 'rider':
            return redirect('rider_dashboard')
    return render(request, 'home.html')

@login_required
def customer_dashboard(request):
    if request.user.user_type != 'customer':
        return redirect('home')
    
    try:
        customer_profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        # Create customer profile if it doesn't exist
        customer_profile = CustomerProfile.objects.create(user=request.user)
    
    # Get customer's orders
    orders = Order.objects.filter(customer=customer_profile).order_by('-created_at')
    
    # Get customer's addresses
    addresses = CustomerAddress.objects.filter(customer=request.user)
    
    context = {
        'orders': orders,
        'addresses': addresses,
    }
    return render(request, 'accounts/customer_dashboard.html', context)

@login_required
def business_dashboard(request):
    if request.user.user_type != 'business':
        return redirect('home')
    return render(request, 'accounts/business_dashboard.html')

@login_required
def rider_dashboard(request):
    if request.user.user_type != 'rider':
        return redirect('home')
    return render(request, 'accounts/rider_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home') 