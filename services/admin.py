from django.contrib import admin
from .models import Service, Tag, ServiceOption, BusinessLocation, BusinessSchedule, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'business__business_name')
    raw_id_fields = ('business', 'category')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'is_available')
    list_filter = ('service', 'is_available')
    search_fields = ('name', 'service__name')
    raw_id_fields = ('service',)

@admin.register(BusinessLocation)
class BusinessLocationAdmin(admin.ModelAdmin):
    list_display = ('business', 'address', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('business__business_name', 'address')
    raw_id_fields = ('business',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BusinessSchedule)
class BusinessScheduleAdmin(admin.ModelAdmin):
    list_display = ('business', 'day', 'opening_time', 'closing_time', 'is_closed')
    list_filter = ('day', 'is_closed')
    search_fields = ('business__business_name',)
    raw_id_fields = ('business',)
