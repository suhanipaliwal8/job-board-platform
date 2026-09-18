from django.urls import path

from .views import (
    ResumeUploadView,
    MyResumeView,
    ApplyForJobView,
    MyApplicationsView,
    EmployerApplicationsView,
    ApplicationStatusUpdateView,
    EmployerNotificationsView,
    CandidateApplicationUpdateView,
    CandidateApplicationDeleteView,
)


urlpatterns = [

    path(
        "resume/",
        ResumeUploadView.as_view(),
        name="resume-upload"
    ),

    path(
        "resume/me/",
        MyResumeView.as_view(),
        name="my-resume"
    ),

    path(
        "apply/",
        ApplyForJobView.as_view(),
        name="apply-job"
    ),

    path(
        "my/",
        MyApplicationsView.as_view(),
        name="my-applications"
    ),

    path(
        "employer/",
        EmployerApplicationsView.as_view(),
        name="employer-applications"
    ),

    path(
        "<int:pk>/status/",
        ApplicationStatusUpdateView.as_view(),
        name="application-status"
    ),

    path(
        "notifications/",
        EmployerNotificationsView.as_view()
    ),

    path(
        "<int:pk>/update/",
        CandidateApplicationUpdateView.as_view(),
        name="application-update"
    ),

    path(
        "<int:pk>/delete/",
        CandidateApplicationDeleteView.as_view()
    ),
]