from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def login_page(request):
    return render(request, "login.html")


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