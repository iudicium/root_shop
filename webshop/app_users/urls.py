from django.urls import path
from .views import (
    LoginView,
    LogOutView,
    SignUpView,
    ProfileView,
    AvatarUpdateView,
    PasswordUpdateView,
)


app_name = "app_users"

urlpatterns = [
    path("sign-in", LoginView.as_view(), name="sign-in"),
    path("sign-up", SignUpView.as_view(), name="sign-up"),
    path("sign-out", LogOutView.as_view(), name="sign-out"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/avatar", AvatarUpdateView.as_view(), name="avatar-update"),
    path("profile/password", PasswordUpdateView.as_view(), name="password-update"),
]
