from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.order_create, name="order_create"),
    path("<int:pk>/", views.order_detail, name="order_detail"),
    path("<int:pk>/edit/", views.order_edit, name="order_edit"),
    path("<int:pk>/delete/", views.order_delete, name="order_delete"),
    path("<int:pk>/status/", views.order_status_update, name="order_status_update"),

    # Customer storefront
    path("shop/", views.storefront, name="storefront"),
    path("shop/buy/<int:product_id>/", views.buy_now, name="buy_now"),
    path("shop/my-orders/", views.my_orders, name="my_orders"),
]