# customers/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import Customer, Company
import json


@csrf_exempt
@require_http_methods(["POST"])
def contact_submission(request):
    """Handle contact form submissions from website"""
    try:
        data = json.loads(request.body)
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()
        company = data.get("company", "").strip()

        if not all([name, email, message]):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Name, email, and message are required.",
                },
                status=400,
            )

        # Split name
        name_parts = name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Create or get company
        company_obj = None
        if company:
            company_obj, created = Company.objects.get_or_create(
                name=company, defaults={"industry": "Unknown"}
            )

        # Create customer record
        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "company": company_obj,
                "lead_source": "Website Contact Form",
                "lead_status": "new",
            },
        )

        # TODO: Send email notification to sales team
        # TODO: Create interaction record with message

        return JsonResponse(
            {
                "status": "success",
                "message": "Thank you for your interest! Our team will contact you soon.",
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid data format."}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": "An error occurred. Please try again."},
            status=500,
        )


@csrf_exempt
@require_http_methods(["POST"])
def trial_signup(request):
    """Handle free trial signups"""
    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        company = data.get("company", "").strip()

        if not all([email, first_name]):
            return JsonResponse(
                {"status": "error", "message": "Email and first name are required."},
                status=400,
            )

        # Create company if provided
        company_obj = None
        if company:
            company_obj, created = Company.objects.get_or_create(
                name=company, defaults={"industry": "Unknown"}
            )

        # Create customer record
        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "company": company_obj,
                "lead_source": "Free Trial Signup",
                "lead_status": "new",
            },
        )

        # Create user account for portal access
        if created:
            user, user_created = User.objects.get_or_create(
                username=email,
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
                },
            )

            if user_created:
                # Set temporary password (should be sent via email)
                temp_password = "temp123"  # In production, generate random password
                user.set_password(temp_password)
                user.save()

        return JsonResponse(
            {
                "status": "success",
                "message": "Trial account created! Check your email for login details.",
                "redirect": "/portal/login/",
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid data format."}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": "An error occurred. Please try again."},
            status=500,
        )
