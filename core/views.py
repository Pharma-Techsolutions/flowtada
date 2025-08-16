# core/views.py

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class HomeView(TemplateView):
    """Main landing page"""

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "FlowTada - CRM Solutions for Growing Businesses",
                "meta_description": "Transform your business with smart CRM solutions. FlowTada helps SMBs streamline customer relationships and boost sales.",
            }
        )
        return context


def about_view(request):
    """About page"""
    return render(
        request, "core/about.html", {"page_title": "About FlowTada - Your CRM Partner"}
    )


def pricing_view(request):
    """Pricing page"""
    pricing_plans = [
        {
            "name": "Starter",
            "price": 29,
            "features": ["Up to 1,000 contacts", "Basic reporting", "Email support"],
            "recommended": False,
        },
        {
            "name": "Professional",
            "price": 79,
            "features": [
                "Up to 10,000 contacts",
                "Advanced analytics",
                "Priority support",
                "API access",
            ],
            "recommended": True,
        },
        {
            "name": "Enterprise",
            "price": 199,
            "features": [
                "Unlimited contacts",
                "Custom integrations",
                "24/7 phone support",
                "Dedicated account manager",
            ],
            "recommended": False,
        },
    ]

    return render(
        request,
        "core/pricing.html",
        {
            "page_title": "FlowTada Pricing - Choose Your Plan",
            "pricing_plans": pricing_plans,
        },
    )


@csrf_exempt
def contact_form(request):
    """Handle contact form submissions"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            message = data.get("message")

            # TODO: Save to database and send email
            # For now, just return success

            return JsonResponse(
                {"status": "success", "message": "Thank you! We'll be in touch soon."}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid data format"}, status=400
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )
