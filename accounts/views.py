from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "Registration successful",
                    "username": user.username,
                    "role": user.profile.role,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        return Response(
            {
                "message": "Login successful",
                "username": user.username,
                "role": user.profile.role,
            }
        )


class LogoutView(APIView):

    def post(self, request):

        logout(request)

        return Response(
            {"message": "Logout successful"}
        )


class ProfileView(APIView):

    def get(self, request):

        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = request.user
        profile = user.profile

        return Response(
            {
                "username": user.username,
                "email": user.email,
                "role": profile.role,
                "phone": profile.phone,
                "company_name": profile.company_name,
            }
        )