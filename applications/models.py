from django.db import models
from django.contrib.auth.models import User

from jobs.models import Job


class Resume(models.Model):

    candidate = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="resume"
    )

    resume_file = models.FileField(
        upload_to="resumes/"
    )

    uploaded_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.candidate.username}'s Resume"


class Application(models.Model):

    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("selected", "Selected"),
    ]

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "job"],
                name="unique_candidate_job_application"
            )
        ]

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"