# flowtada/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Non-translated URLs (like API endpoints)
urlpatterns = [
    # Language switching URL
    path('i18n/', include('django.conf.urls.i18n')),
    # path('api/', include('core.api_urls')),  # API doesn't need translation
]

# Translated URLs
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('portal/', include('portal.urls')),
    path('customers/', include('customers.urls')),
    path('analytics/', include('analytics.urls')),
    # path('companies/', include('companies.urls')),
    prefix_default_language=False,  # Don't add /en/ for default language
)

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "FlowTada CRM Administration"
admin.site.site_title = "FlowTada Admin"
admin.site.index_title = "Welcome to FlowTada CRM"