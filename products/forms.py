from django import forms
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Category name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Category description"
            }),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "sku", "category", "description",
            "price", "cost_price", "stock_quantity",
            "low_stock_threshold", "image", "is_active"
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Product name"
            }),
            "sku": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. PRD-001"
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Product description"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price"
            }),
            "cost_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Cost price"
            }),
            "stock_quantity": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "low_stock_threshold": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }