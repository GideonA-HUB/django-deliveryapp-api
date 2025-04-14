from django.contrib import admin
from .models import Order, OrderItem, OrderStatus

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'business', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'customer__email', 'business__business_name')
    raw_id_fields = ('customer', 'business')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'service__name')
    raw_id_fields = ('order', 'service')

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id',)
    raw_id_fields = ('order',)
    readonly_fields = ('created_at',)
