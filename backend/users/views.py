from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterUserSerializer

# Create your views here.


class Register(APIView):

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message ": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()
        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect username or password")
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Optionally set tokens in cookies (optional)
        response = Response(
            {
                "message": "Login successful",
            }
        )
        response.set_cookie(
            key="auth_token",
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response

    #   payload = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=60)}
    #   return Response(
    #       {"message": "Login successful", "payload": payload},
    #       status=status.HTTP_200_OK,
    #   )
