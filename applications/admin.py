from django.contrib import admin
from .models import Resume, Application, Notification


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("candidate", "uploaded_at")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("candidate__username", "job__title")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("employer", "message", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("employer__username", "message")