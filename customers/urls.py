# customers/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "customers"

# For future API endpoints
router = DefaultRouter()
# router.register(r'customers', views.CustomerViewSet)
# router.register(r'deals', views.DealViewSet)

urlpatterns = [
    # API routes (for future mobile app/integrations)
    path("", include(router.urls)),
    # Web endpoints
    path("contact/", views.contact_submission, name="contact"),
    path("trial/", views.trial_signup, name="trial_signup"),
]
