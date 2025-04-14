from django import forms
from .models import Order, OrderItem, CartItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_instructions']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'delivery_instructions': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['service', 'quantity', 'special_instructions']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'special_instructions': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['service', 'quantity', 'special_instructions']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'special_instructions': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity 