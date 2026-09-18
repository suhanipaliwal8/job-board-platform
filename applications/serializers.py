from rest_framework import serializers

from .models import Resume, Application, Notification


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

    candidate = serializers.CharField(
        source="candidate.username",
        read_only=True
    )

    job = serializers.IntegerField(
        source="job.id",
        read_only=True
    )

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="job.company_name",
        read_only=True
    )

    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Application

        fields = [
            "id",
            "candidate",
            "job",
            "job_title",
            "company_name",
            "resume_url",
            "cover_letter",
            "status",
            "applied_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "job",
            "job_title",
            "company_name",
            "resume_url",
            "status",
            "applied_at",
            "updated_at",
        ]

    def get_resume_url(self, obj):

        try:
            request = self.context.get("request")

            if obj.candidate.resume.resume_file:

                url = obj.candidate.resume.resume_file.url

                if request:
                    return request.build_absolute_uri(url)

                return url

        except Exception:
            pass

        return None
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("employer", "created_at")