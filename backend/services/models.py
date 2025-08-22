from django.conf import settings
from django.db import models
from django.core.validators import MaxLengthValidator


class ServiceRequest(models.Model):
    class Category(models.TextChoices):
        DOG_SITTER = "dog_sitter", "Dog Sitter"
        PET_SITTER = "pet_sitter", "Pet Sitter"
        BABYSITTER = "babysitter", "Babysitter"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        CANCELLED = "cancelled", "Cancelled"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_requests", null=True, blank=True)
    notes = models.TextField(blank=True, default="", validators=[MaxLengthValidator(500)])
    # step 1
    category = models.CharField(max_length=20, choices=Category.choices)

    # step 2
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    time_from = models.TimeField(null=True, blank=True)
    hours = models.PositiveSmallIntegerField(default=1)  # 1..24
    days_of_week = models.CharField(max_length=32, blank=True, default="")  # "mon,tue,fri"
    notes = models.TextField(blank=True, default="")

    # step 3
    extra = models.JSONField(default=dict)

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    current_step = models.PositiveSmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ServiceImage(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="requests/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
