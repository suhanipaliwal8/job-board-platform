from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Resume, Application
from .serializers import ResumeSerializer, ApplicationSerializer
from .permissions import IsCandidate, IsEmployer

from jobs.models import Job


class ResumeUploadView(generics.CreateAPIView):

    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsCandidate]

    def create(self, request, *args, **kwargs):

        resume = Resume.objects.filter(
            candidate=request.user
        ).first()

        if resume:
            serializer = self.get_serializer(
                resume,
                data=request.data,
                partial=True
            )
        else:
            serializer = self.get_serializer(
                data=request.data
            )

        serializer.is_valid(raise_exception=True)

        serializer.save(
            candidate=request.user
        )

        return Response(
            {
                "message": "Resume uploaded successfully",
                "resume": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class MyResumeView(generics.RetrieveAPIView):

    serializer_class = ResumeSerializer
    permission_classes = [IsCandidate]

    def get_object(self):

        return Resume.objects.get(
            candidate=self.request.user
        )

class ApplyForJobView(generics.CreateAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

    def create(self, request, *args, **kwargs):

        job_id = request.data.get("job")

        try:
            job = Job.objects.get(
                id=job_id,
                is_active=True
            )
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not hasattr(request.user, "resume"):
            return Response(
                {
                    "error": "Please upload your resume before applying."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if Application.objects.filter(
            candidate=request.user,
            job=job
        ).exists():

            return Response(
                {
                    "error": "You have already applied for this job."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        application = Application.objects.create(
            candidate=request.user,
            job=job
        )

        serializer = self.get_serializer(application)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class MyApplicationsView(generics.ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):

        return Application.objects.filter(
            candidate=self.request.user
        ).select_related(
            "job"
        ).order_by("-applied_at")

class EmployerApplicationsView(generics.ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):

        return Application.objects.filter(
            job__employer=self.request.user
        ).select_related(
            "candidate",
            "job"
        ).order_by("-applied_at")

class ApplicationStatusUpdateView(generics.UpdateAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsEmployer]

    queryset = Application.objects.all()

    http_method_names = ["patch"]

    def update(self, request, *args, **kwargs):

        application = self.get_object()

        if application.job.employer != request.user:

            return Response(
                {
                    "error": "You can only update applications for your own jobs."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")

        valid_statuses = [
            "applied",
            "shortlisted",
            "rejected",
            "selected",
        ]

        if new_status not in valid_statuses:

            return Response(
                {
                    "error": "Invalid application status."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        serializer = self.get_serializer(application)

        return Response(serializer.data)