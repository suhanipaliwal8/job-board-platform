from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company_name",
        "location",
        "job_type",
        "experience",
        "is_active",
        "created_at",
    )

    list_filter = (
        "job_type",
        "experience",
        "is_active",
        "location",
    )

    search_fields = (
        "title",
        "company_name",
        "location",
        "skills",
    )