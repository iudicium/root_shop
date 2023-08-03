from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def avatar_directory(instance, filename):
    return f"avatars/{str(instance)}/{filename}"


class Avatar(models.Model):
    src = models.ImageField(
        upload_to=avatar_directory, default="avatars/default.jpg", verbose_name="Image"
    )
    alt = models.CharField(max_length=128, verbose_name="Description")

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"

    def __str__(self):
        return self.alt


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    email = models.EmailField(verbose_name="Email", blank=True)
    fullName = models.CharField(max_length=128, verbose_name="Full Name")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Phone Number"
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Balance"
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Avatar",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"User: {self.user.username}\nFull Name: {self.fullName}"
