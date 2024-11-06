from django.contrib import admin
from django.urls import path, include
from inventory.views import access_denied

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('access-denied/', access_denied, name='access_denied'),
] 