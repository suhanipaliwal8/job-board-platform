"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from .frontend_views import (
    home,
    login_page,
    register_page,
    candidate_dashboard,
    employer_dashboard,
    job_detail,
)

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    # Frontend

    path(
        "",
        home,
        name="home"
    ),

    path(
        "login/",
        login_page,
        name="login-page"
    ),

    path(
        "register/",
        register_page,
        name="register-page"
    ),

    path(
        "candidate-dashboard/",
        candidate_dashboard,
        name="candidate-dashboard"
    ),

    path(
        "employer-dashboard/",
        employer_dashboard,
        name="employer-dashboard"
    ),

    path(
        "jobs/<int:job_id>/",
        job_detail,
        name="job-detail-page"
    ),


    # APIs

    path(
        "api/accounts/",
        include("accounts.urls")
    ),

    path(
        "api/jobs/",
        include("jobs.urls")
    ),

    path(
        "api/applications/",
        include("applications.urls")
    ),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )