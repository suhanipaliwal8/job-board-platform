from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=["candidate", "employer"]
    )
    company_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "role",
            "company_name",
        ]

    def create(self, validated_data):

        role = validated_data.pop("role")
        company_name = validated_data.pop("company_name", "")

        user = User.objects.create_user(
            **validated_data
        )

        profile = user.profile
        profile.role = role
        profile.company_name = company_name
        profile.save()

        return user