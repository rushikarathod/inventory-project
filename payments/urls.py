from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_list, name="payment_list"),
    path("create/<int:order_pk>/", views.payment_create, name="payment_create"),
    path("<int:pk>/", views.payment_detail, name="payment_detail"),
    path("<int:pk>/edit/", views.payment_edit, name="payment_edit"),
    path("<int:pk>/status/", views.payment_status_update, name="payment_status_update"),
]