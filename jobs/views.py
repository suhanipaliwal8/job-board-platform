from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Job
from .serializers import JobSerializer
from .permissions import IsEmployer


class JobListCreateView(generics.ListCreateAPIView):

    serializer_class = JobSerializer

    def get_queryset(self):

        queryset = Job.objects.filter(
            is_active=True
        ).order_by("-created_at")

        search = self.request.query_params.get("search")

        location = self.request.query_params.get("location")

        job_type = self.request.query_params.get("job_type")

        experience = self.request.query_params.get("experience")

        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                skills__icontains=search
            ) | queryset.filter(
                company_name__icontains=search
            )

        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        if job_type:
            queryset = queryset.filter(
                job_type=job_type
            )

        if experience:
            queryset = queryset.filter(
                experience=experience
            )

        return queryset

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsEmployer()]

        return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):

        serializer.save(
            employer=self.request.user
        )


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def get_permissions(self):

        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsEmployer()]

        return [IsAuthenticatedOrReadOnly()]

    def perform_update(self, serializer):

        job = self.get_object()

        if job.employer != self.request.user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You can only modify your own jobs."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if instance.employer != self.request.user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You can only delete your own jobs."
            )

        instance.delete()