from rest_framework import serializers

from .models import Resume, Application


class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume

        fields = [
            "id",
            "resume_file",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_at",
        ]


class ApplicationSerializer(serializers.ModelSerializer):

    candidate = serializers.ReadOnlyField(
        source="candidate.username"
    )

    job_title = serializers.ReadOnlyField(
        source="job.title"
    )

    company_name = serializers.ReadOnlyField(
        source="job.company_name"
    )

    class Meta:
        model = Application

        fields = [
            "id",
            "candidate",
            "job",
            "job_title",
            "company_name",
            "status",
            "applied_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "status",
            "applied_at",
            "updated_at",
        ]