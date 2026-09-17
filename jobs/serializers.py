from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    employer = serializers.ReadOnlyField(
        source="employer.username"
    )

    class Meta:
        model = Job

        fields = [
            "id",
            "employer",
            "title",
            "description",
            "company_name",
            "location",
            "salary",
            "job_type",
            "experience",
            "skills",
            "created_at",
            "updated_at",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "employer",
            "created_at",
            "updated_at",
        ]