from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BusinessProfile, CustomerProfile, RiderProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'user_type'),
        }),
    )

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'business_type', 'user', 'is_verified')
    list_filter = ('business_type', 'is_verified')
    search_fields = ('business_name', 'user__email')
    raw_id_fields = ('user',)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'created_at')
    search_fields = ('user__email', 'address')
    raw_id_fields = ('user',)

@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'license_number', 'is_available')
    list_filter = ('vehicle_type', 'is_available')
    search_fields = ('user__email', 'license_number')
    raw_id_fields = ('user',)
