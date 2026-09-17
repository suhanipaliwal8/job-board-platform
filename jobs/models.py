from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
    ]

    EXPERIENCE_CHOICES = [
        ("fresher", "Fresher"),
        ("1-2", "1-2 Years"),
        ("3-5", "3-5 Years"),
        ("5+", "5+ Years"),
    ]

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=150)

    description = models.TextField()

    company_name = models.CharField(max_length=150)

    location = models.CharField(max_length=100)

    salary = models.CharField(max_length=100, blank=True)

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES
    )

    skills = models.CharField(
        max_length=500,
        help_text="Enter skills separated by commas"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title