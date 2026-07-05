from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        CUSTOMER = "customer", "Customer"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"