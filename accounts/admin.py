# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "role", "phone", "is_active"]
    list_filter = ["role", "is_active"]
    search_fields = ["username", "email"]
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role", "phone", "profile_photo")}),
    )