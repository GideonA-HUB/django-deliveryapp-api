from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            
            if request.user.role not in roles:
                return HttpResponseForbidden("Permission denied")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def customer_required(view_func):
    return role_required(['customer'])(view_func)

def business_required(view_func):
    return role_required(['business'])(view_func)

def rider_required(view_func):
    return role_required(['rider'])(view_func)

def verified_email_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required")
        
        if not request.user.is_email_verified:
            return HttpResponseForbidden("Email verification required")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view 