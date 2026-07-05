from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["method", "status", "amount", "transaction_id", "notes"]
        widgets = {
            "method": forms.Select(attrs={
                "class": "form-select"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter amount"
            }),
            "transaction_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. UPI ref / Card last 4 digits"
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Any payment notes..."
            }),
        }


class PaymentStatusForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
        }