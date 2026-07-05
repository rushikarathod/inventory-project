# Register your models here.
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "category", "price", "cost_price", "stock_quantity", "is_active"]
    list_filter = ["is_active", "category"]
    search_fields = ["name", "sku"]