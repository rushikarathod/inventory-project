from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name", "customer_email", "customer_phone",
            "shipping_address", "status", "notes"
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "customer_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "shipping_address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Full shipping address"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Any extra notes..."}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "unit_price"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price per unit"}),
        }


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    extra=1, can_delete=True, min_num=1, validate_min=True,
)


# NEW: Simple checkout form for customer "Buy Now"
class CheckoutForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter your full address"})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact number"})
    )