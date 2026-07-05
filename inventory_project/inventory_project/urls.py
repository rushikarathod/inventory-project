from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard (home page)
    path('', product_views.dashboard, name='dashboard'),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)