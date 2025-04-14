from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BusinessProfile, CustomerProfile, RiderProfile
from .serializers import (
    UserSerializer, BusinessProfileSerializer, CustomerProfileSerializer,
    RiderProfileSerializer, UserRegistrationSerializer, BusinessRegistrationSerializer,
    RiderRegistrationSerializer
)
from .forms import (
    UserRegistrationForm, UserProfileForm,
    UserPasswordChangeForm, UserPasswordResetForm,
    UserSetPasswordForm
)
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        # Create appropriate profile based on user type
        if user.user_type == 'customer':
            CustomerProfile.objects.create(user=user)
        elif user.user_type == 'business':
            BusinessProfile.objects.create(user=user)
        elif user.user_type == 'rider':
            RiderProfile.objects.create(user=user)
        
        # Send activation email
        user.send_activation_email(self.request)
        
        return response

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    next_page = 'accounts:login'

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

class BusinessRegistrationView(generics.CreateAPIView):
    serializer_class = BusinessRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class RiderRegistrationView(generics.CreateAPIView):
    serializer_class = RiderRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class BusinessProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.business_profile

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer_profile

class RiderProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RiderProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.rider_profile

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            # Create profile based on user type
            if user_type == 'customer':
                CustomerProfile.objects.create(
                    user=user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone=form.cleaned_data['phone']
                )
            elif user_type == 'business':
                BusinessProfile.objects.create(
                    user=user,
                    business_name=form.cleaned_data['business_name'],
                    business_type=form.cleaned_data['business_type'],
                    phone=form.cleaned_data['business_phone']
                )
            elif user_type == 'rider':
                RiderProfile.objects.create(
                    user=user,
                    first_name=form.cleaned_data['rider_first_name'],
                    last_name=form.cleaned_data['rider_last_name'],
                    phone=form.cleaned_data['rider_phone'],
                    vehicle_type=form.cleaned_data['vehicle_type']
                )
            
            # Set user type
            user.user_type = user_type
            user.save()
            
            # Log in the user
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)  # Session expires when browser closes
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    user = request.user
    context = {}
    
    if user.user_type == 'customer':
        profile = CustomerProfile.objects.get(user=user)
        context['profile'] = profile
        template = 'accounts/customer_profile.html'
    elif user.user_type == 'business':
        profile = BusinessProfile.objects.get(user=user)
        context['profile'] = profile
        template = 'accounts/business_profile.html'
    elif user.user_type == 'rider':
        profile = RiderProfile.objects.get(user=user)
        context['profile'] = profile
        template = 'accounts/rider_profile.html'
    
    return render(request, template, context)

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        user = request.user
        if user.user_type == 'customer':
            profile = CustomerProfile.objects.get(user=user)
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
            profile.phone = request.POST.get('phone')
            profile.save()
        elif user.user_type == 'business':
            profile = BusinessProfile.objects.get(user=user)
            profile.business_name = request.POST.get('business_name')
            profile.business_type = request.POST.get('business_type')
            profile.phone = request.POST.get('phone')
            profile.save()
        elif user.user_type == 'rider':
            profile = RiderProfile.objects.get(user=user)
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
            profile.phone = request.POST.get('phone')
            profile.vehicle_type = request.POST.get('vehicle_type')
            profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return redirect('profile')

class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password-change-done')

class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password-reset-done')

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password-reset-complete')

class UserActivationView(TemplateView):
    template_name = 'accounts/activation.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return self.render_to_response({'success': True})
        else:
            return self.render_to_response({'success': False})
