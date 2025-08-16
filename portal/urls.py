# portal/urls.py

from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("deals/", views.deals_view, name="deals"),
    path("interactions/", views.interactions_view, name="interactions"),
]
