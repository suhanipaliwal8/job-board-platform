from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def home(request):
    return render(request, "index.html")

@ensure_csrf_cookie
def login_page(request):
    return render(request, "login.html")

@ensure_csrf_cookie
def register_page(request):
    return render(request, "register.html")


def candidate_dashboard(request):
    return render(
        request,
        "candidate_dashboard.html"
    )


def employer_dashboard(request):
    return render(
        request,
        "employer_dashboard.html"
    )


def job_detail(request, job_id):
    return render(
        request,
        "job_detail.html",
        {"job_id": job_id}
    )