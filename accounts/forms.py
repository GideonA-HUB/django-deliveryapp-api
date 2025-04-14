from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
    PasswordChangeForm, PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model
from .models import CustomerProfile, BusinessProfile, RiderProfile

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class UserPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ('email',)

class UserSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('address',)

class BusinessProfileForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        help_text="Please include the following information in your description:\n"
                 "- Business address\n"
                 "- City and state\n"
                 "- ZIP code\n"
                 "- Phone number\n"
                 "- Website (if applicable)\n"
                 "- Opening hours\n"
                 "Example:\n"
                 "123 Business St, City, State 12345\n"
                 "Phone: (555) 123-4567\n"
                 "Website: www.example.com\n"
                 "Hours: Mon-Fri 9am-5pm, Sat 10am-2pm"
    )

    class Meta:
        model = BusinessProfile
        fields = ('business_name', 'business_type', 'description')

class RiderProfileForm(forms.ModelForm):
    class Meta:
        model = RiderProfile
        fields = ('vehicle_type', 'license_number') 