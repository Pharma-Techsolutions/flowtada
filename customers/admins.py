# customers/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Company, Customer, Interaction, Deal


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "industry", "size", "website", "created_at"]
    list_filter = ["industry", "size", "created_at"]
    search_fields = ["name", "website"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("name", "website", "industry", "size")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


class InteractionInline(admin.TabularInline):
    model = Interaction
    extra = 1
    readonly_fields = ["created_at"]
    fields = ["interaction_type", "subject", "notes", "user", "created_at"]


class DealInline(admin.TabularInline):
    model = Deal
    extra = 1
    readonly_fields = ["created_at", "updated_at"]
    fields = [
        "title",
        "value",
        "stage",
        "probability",
        "expected_close_date",
        "assigned_to",
    ]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "email",
        "company",
        "lead_status",
        "assigned_to",
        "created_at",
        "last_contacted",
    ]
    list_filter = ["lead_status", "lead_source", "assigned_to", "created_at"]
    search_fields = ["first_name", "last_name", "email", "company__name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "email", "phone")},
        ),
        ("Company Information", {"fields": ("company", "position")}),
        (
            "CRM Fields",
            {"fields": ("lead_status", "lead_source", "assigned_to", "last_contacted")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    inlines = [InteractionInline, DealInline]

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = "Name"


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ["customer", "interaction_type", "subject", "user", "created_at"]
    list_filter = ["interaction_type", "user", "created_at"]
    search_fields = ["customer__first_name", "customer__last_name", "subject", "notes"]
    readonly_fields = ["created_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("customer", "user")


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "customer",
        "value",
        "stage",
        "probability",
        "expected_close_date",
        "assigned_to",
        "created_at",
    ]
    list_filter = ["stage", "assigned_to", "created_at", "expected_close_date"]
    search_fields = ["title", "customer__first_name", "customer__last_name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Deal Information", {"fields": ("customer", "title", "value")}),
        (
            "Sales Process",
            {"fields": ("stage", "probability", "expected_close_date", "assigned_to")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("customer", "assigned_to")

    # Custom admin styling
    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}
