# customers/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Company(models.Model):
    """Company/Organization model"""

    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    size = models.CharField(
        max_length=50,
        choices=[
            ("1-10", "1-10 employees"),
            ("11-50", "11-50 employees"),
            ("51-200", "51-200 employees"),
            ("201-1000", "201-1000 employees"),
            ("1000+", "1000+ employees"),
        ],
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Customer contact model"""

    LEAD_STATUS_CHOICES = [
        ("new", "New Lead"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("proposal", "Proposal Sent"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )
    position = models.CharField(max_length=100, blank=True)

    # CRM fields
    lead_status = models.CharField(
        max_length=20, choices=LEAD_STATUS_CHOICES, default="new"
    )
    lead_source = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("customers:detail", kwargs={"pk": self.pk})


class Interaction(models.Model):
    """Customer interaction/activity log"""

    INTERACTION_TYPES = [
        ("call", "Phone Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("demo", "Demo"),
        ("proposal", "Proposal"),
        ("follow_up", "Follow Up"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="interactions"
    )
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    subject = models.CharField(max_length=200)
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.interaction_type}: {self.subject}"


class Deal(models.Model):
    """Sales deal/opportunity"""

    DEAL_STAGES = [
        ("prospecting", "Prospecting"),
        ("qualification", "Qualification"),
        ("proposal", "Proposal"),
        ("negotiation", "Negotiation"),
        ("closed_won", "Closed Won"),
        ("closed_lost", "Closed Lost"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="deals"
    )
    title = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=20, choices=DEAL_STAGES, default="prospecting")
    probability = models.IntegerField(
        default=10, help_text="Probability of closing (0-100%)"
    )
    expected_close_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - ${self.value}"
