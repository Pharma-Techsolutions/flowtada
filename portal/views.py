# portal/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customers.models import Customer, Deal, Interaction
import json


def login_view(request):
    """Customer portal login"""
    if request.user.is_authenticated:
        return redirect("portal:dashboard")

    if request.method == "POST":
        if request.content_type == "application/json":
            # Handle AJAX login
            try:
                data = json.loads(request.body)
                username = data.get("email")
                password = data.get("password")

                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return JsonResponse(
                        {"status": "success", "redirect": "/portal/dashboard/"}
                    )
                else:
                    return JsonResponse(
                        {"status": "error", "message": "Invalid email or password"}
                    )
            except json.JSONDecodeError:
                return JsonResponse(
                    {"status": "error", "message": "Invalid data format"}
                )
        else:
            # Handle form submission
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name}!")
                    return redirect("portal:dashboard")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()

    return render(request, "portal/login.html", {"form": form})


@login_required
def dashboard_view(request):
    """Customer portal dashboard"""
    # Get customer data for the logged-in user
    try:
        customer = Customer.objects.get(email=request.user.email)

        # Get customer's deals
        deals = Deal.objects.filter(customer=customer).order_by("-created_at")[:5]

        # Get recent interactions
        interactions = Interaction.objects.filter(customer=customer).order_by(
            "-created_at"
        )[:5]

        # Calculate stats
        total_deals = deals.count()
        won_deals = deals.filter(stage="closed_won").count()
        total_value = sum(deal.value for deal in deals)

        context = {
            "customer": customer,
            "deals": deals,
            "interactions": interactions,
            "stats": {
                "total_deals": total_deals,
                "won_deals": won_deals,
                "total_value": total_value,
                "success_rate": round(
                    (won_deals / total_deals * 100) if total_deals > 0 else 0, 1
                ),
            },
        }

    except Customer.DoesNotExist:
        # User doesn't have a customer record
        context = {
            "customer": None,
            "message": "No customer record found. Please contact support.",
        }

    return render(request, "portal/dashboard.html", context)


@login_required
def profile_view(request):
    """Customer profile management"""
    try:
        customer = Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect("portal:dashboard")

    if request.method == "POST":
        # Update customer information
        customer.first_name = request.POST.get("first_name", customer.first_name)
        customer.last_name = request.POST.get("last_name", customer.last_name)
        customer.phone = request.POST.get("phone", customer.phone)
        customer.position = request.POST.get("position", customer.position)
        customer.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("portal:profile")

    return render(request, "portal/profile.html", {"customer": customer})


@login_required
def deals_view(request):
    """Customer deals list"""
    try:
        customer = Customer.objects.get(email=request.user.email)
        deals = Deal.objects.filter(customer=customer).order_by("-created_at")
    except Customer.DoesNotExist:
        deals = []

    return render(request, "portal/deals.html", {"deals": deals})


@login_required
def interactions_view(request):
    """Customer interactions history"""
    try:
        customer = Customer.objects.get(email=request.user.email)
        interactions = Interaction.objects.filter(customer=customer).order_by(
            "-created_at"
        )
    except Customer.DoesNotExist:
        interactions = []

    return render(request, "portal/interactions.html", {"interactions": interactions})


def logout_view(request):
    """Customer portal logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:home")
