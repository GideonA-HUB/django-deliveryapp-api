from django import forms
from .models import Delivery

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('order', 'rider', 'status')
        widgets = {
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'delivery_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        pickup_time = cleaned_data.get('pickup_time')
        delivery_time = cleaned_data.get('delivery_time')

        if pickup_time and delivery_time and pickup_time >= delivery_time:
            raise forms.ValidationError("Delivery time must be after pickup time.")

        return cleaned_data

class DeliveryUpdateForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'}) 