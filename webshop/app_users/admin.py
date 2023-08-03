from django.contrib import admin
from .models import Profile, Avatar

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "fullName",
        "phone",
        "avatar",
    )


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    fields = (
        "src",
        "alt",
    )
