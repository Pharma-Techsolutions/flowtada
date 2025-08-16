# flowtada/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Main website
    path('portal/', include('portal.urls')),  # Customer portal
    path('api/', include('customers.urls')),  # API endpoints
    path('analytics/', include('analytics.urls')),  # Dashboard
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "FlowTada CRM Administration"
admin.site.site_title = "FlowTada Admin"
admin.site.index_title = "Welcome to FlowTada CRM"