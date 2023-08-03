from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from .models import Profile, Avatar
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from json import loads
from .serializers import ProfileSerializer


# Create your views here.
class LoginView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request: Request) -> Response(status):
        serialized_data = list(request.POST.keys())[0]
        user_data = loads(serialized_data)
        username = user_data.get("username", None)
        password = user_data.get("password", None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request: Request) -> Response(status):
        serialized_data = list(request.data.keys())[0]
        user_data = loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            Profile.objects.create(user=user, fullName=name)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogOutView(APIView):
    def post(self, request: Request) -> Response(status):
        logout(request)
        return status.HTTP_200_OK


class ProfileView(APIView):
    def get(self, request: Request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)

            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class AvatarUpdateView(APIView):
    def post(self, request: Request) -> Response(status):
        try:
            profile_image = request.FILES["avatar"]

            profile = Profile.objects.get(user=request.user)
            avatar = Avatar.objects.create(src=profile_image, alt=f"{request.user}")
            profile.avatar = avatar
            profile.save()
            return Response(status.HTTP_200_OK)
        except Exception as e:
            print(e)


class PasswordUpdateView(APIView):
    def post(self, request: Request) -> Response(status):
        user = request.user
        old_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")

        if not user.check_password(old_password):
            return Response(
                {"detail": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
        )
