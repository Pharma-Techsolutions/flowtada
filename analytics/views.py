# analytics/views.py

from django.shortcuts import render


# Future analytics views will go here
def dashboard_view(request):
    return render(request, "analytics/dashboard.html")
