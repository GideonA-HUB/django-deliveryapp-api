from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Order, OrderItem, Cart, CartItem
from .forms import OrderForm, CartItemForm
from django.db.models import Prefetch
from accounts.models import CustomerProfile

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        return Order.objects.filter(customer=customer_profile).order_by('-created_at')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        return Order.objects.filter(customer=customer_profile).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('service'))
        )

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order-list')

    def form_valid(self, form):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        form.instance.customer = customer_profile
        response = super().form_valid(form)
        
        # Move items from cart to order
        cart = Cart.objects.get(customer=customer_profile)
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=self.object,
                service=cart_item.service,
                quantity=cart_item.quantity,
                price=cart_item.service.price
            )
        
        # Clear the cart
        cart.items.all().delete()
        
        messages.success(self.request, 'Order created successfully!')
        return response

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def get_queryset(self):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        return Order.objects.filter(customer=customer_profile)

    def get_success_url(self):
        return reverse_lazy('orders:order-detail', kwargs={'pk': self.object.pk})

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order-list')

    def get_queryset(self):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        return Order.objects.filter(customer=customer_profile)

class CartView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'orders/cart.html'
    context_object_name = 'cart'

    def get_object(self):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        cart, created = Cart.objects.get_or_create(customer=customer_profile)
        return cart

class AddToCartView(LoginRequiredMixin, CreateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'orders/add_to_cart.html'

    def form_valid(self, form):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        cart, created = Cart.objects.get_or_create(customer=customer_profile)
        form.instance.cart = cart
        
        # Check if item already exists in cart
        existing_item = cart.items.filter(service=form.instance.service).first()
        if existing_item:
            existing_item.quantity += form.instance.quantity
            existing_item.save()
            messages.success(self.request, 'Cart updated successfully!')
            return redirect('orders:cart')
        
        response = super().form_valid(form)
        messages.success(self.request, 'Item added to cart!')
        return response

    def get_success_url(self):
        return reverse_lazy('orders:cart')

class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = 'orders/remove_from_cart.html'
    success_url = reverse_lazy('orders:cart')

    def get_queryset(self):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        return CartItem.objects.filter(cart__customer=customer_profile)

class UpdateCartItemView(LoginRequiredMixin, UpdateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'orders/update_cart_item.html'
    success_url = reverse_lazy('orders:cart')

    def get_queryset(self):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        return CartItem.objects.filter(cart__customer=customer_profile)

class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        cart = Cart.objects.get(customer=customer_profile)
        context['cart'] = cart
        return context

    def form_valid(self, form):
        customer_profile = get_object_or_404(CustomerProfile, user=self.request.user)
        if not customer_profile.cart.items.exists():
            messages.error(self.request, 'Your cart is empty!')
            return redirect('orders:cart')
        
        form.instance.customer = customer_profile
        response = super().form_valid(form)
        
        # Create order items from cart
        cart = customer_profile.cart
        for item in cart.items.all():
            OrderItem.objects.create(
                order=self.object,
                service=item.service,
                quantity=item.quantity,
                price=item.service.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(self.request, 'Order placed successfully!')
        return response

    def get_success_url(self):
        return reverse_lazy('orders:order-detail', kwargs={'pk': self.object.pk}) 