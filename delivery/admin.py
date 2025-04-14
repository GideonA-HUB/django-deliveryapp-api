from django.contrib import admin
from .models import DeliveryAssignment, DeliveryZone, DeliveryFee, DeliveryRating, DeliveryLocation, ZoneBoundary

@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'rider', 'status', 'assigned_at', 'delivered_at')
    list_filter = ('status', 'assigned_at', 'delivered_at')
    search_fields = ('id', 'order__id', 'rider__user__email')
    raw_id_fields = ('order', 'rider')
    readonly_fields = ('assigned_at', 'delivered_at')

@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'latitude', 'longitude', 'timestamp', 'speed')
    list_filter = ('timestamp',)
    search_fields = ('assignment__id',)
    raw_id_fields = ('assignment',)

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_active', 'created_at')
    list_filter = ('is_active', 'city', 'created_at')
    search_fields = ('name', 'city', 'description')
    filter_horizontal = ('businesses',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ZoneBoundary)
class ZoneBoundaryAdmin(admin.ModelAdmin):
    list_display = ('zone', 'latitude', 'longitude', 'order')
    list_filter = ('zone',)
    search_fields = ('zone__name',)
    ordering = ('zone', 'order')

@admin.register(DeliveryFee)
class DeliveryFeeAdmin(admin.ModelAdmin):
    list_display = ('zone', 'min_distance', 'max_distance', 'fee', 'is_active')
    list_filter = ('zone', 'is_active')
    search_fields = ('zone__name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DeliveryRating)
class DeliveryRatingAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'rating', 'created_at', 'created_by')
    list_filter = ('rating', 'created_at')
    search_fields = ('delivery__id', 'comment', 'created_by__email')
    raw_id_fields = ('delivery', 'created_by')
    readonly_fields = ('created_at',)
