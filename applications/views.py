from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Resume, Application, Notification
from .serializers import ResumeSerializer, ApplicationSerializer, NotificationSerializer
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
                {
                    "error": "Job not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )


        # Check resume
        if not hasattr(request.user, "resume"):

            return Response(
                {
                    "error":
                    "Please upload your resume before applying."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        # Check existing application
        existing_application = Application.objects.filter(
            candidate=request.user,
            job=job
        ).first()


        if existing_application:

            # Allow re-apply if previously withdrawn
            if existing_application.status == "withdrawn":

                existing_application.status = "applied"

                existing_application.cover_letter = (
                    request.data.get(
                        "cover_letter",
                        existing_application.cover_letter
                    )
                )

                existing_application.save()


                # Notify employer
                Notification.objects.create(
                    employer=job.employer,
                    message=(
                        f"{request.user.username} "
                        f"re-applied for your job: {job.title}"
                    )
                )


                serializer = self.get_serializer(
                    existing_application
                )

                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )


            # Already applied / shortlisted / rejected / selected
            return Response(
                {
                    "error":
                    "You have already applied for this job."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        # Create new application
        application = Application.objects.create(
            candidate=request.user,
            job=job,
            cover_letter=request.data.get(
                "cover_letter",
                ""
            )
        )


        # Notify employer
        Notification.objects.create(
            employer=job.employer,
            message=(
                f"{request.user.username} "
                f"applied for your job: {job.title}"
            )
        )


        serializer = self.get_serializer(
            application
        )


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

class EmployerNotificationsView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        notifications = Notification.objects.filter(
            employer=request.user
        ).order_by("-created_at")

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class CandidateApplicationUpdateView(generics.UpdateAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):

        return Application.objects.filter(
            candidate=self.request.user
        )

    def update(self, request, *args, **kwargs):

        application = self.get_object()

        if application.status == "withdrawn":

            return Response(
                {
                    "error":
                    "Withdrawn applications cannot be edited."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        application.cover_letter = request.data.get(
            "cover_letter",
            application.cover_letter
        )

        application.save()

        serializer = self.get_serializer(
            application
        )

        return Response(serializer.data)

class CandidateApplicationDeleteView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def delete(self, request, pk):

        try:
            application = Application.objects.select_related(
                "job"
            ).get(
                pk=pk,
                candidate=request.user
            )

        except Application.DoesNotExist:

            return Response(
                {"error": "Application not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if application.status == "withdrawn":

            return Response(
                {"error": "Application is already withdrawn."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Withdraw application
        application.status = "withdrawn"
        application.save()

        # Notify employer
        Notification.objects.create(
            employer=application.job.employer,
            message=(
                f"{request.user.username} "
                f"withdrew their application for "
                f"your job: {application.job.title}"
            )
        )

        return Response(
            {
                "message":
                "Application withdrawn successfully."
            },
            status=status.HTTP_200_OK
        )