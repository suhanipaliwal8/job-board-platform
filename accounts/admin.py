from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "email",
        "role",
        "phone",
        "company_name",
    )

    list_filter = ("role",)

    search_fields = (
        "user__username",
        "user__email",
        "company_name",
    )

    def email(self, obj):
        return obj.user.email

    email.short_description = "Email"