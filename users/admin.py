from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms.models import Room

# Register your models here.


class RoomInline(admin.TabularInline):
    model = Room
    classes = ["collapse"]


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "커스텀 프로필",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "login_method",
        "date_joined",
        "email_verified",
        "email_secret",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "room_count",
    )

    # @admin.register(models.User)
    # class UserAdmin(admin.ModelAdmin):

    #     """Custom User Admin"""

    #     list_display = (
    #         "username",
    #         "email",
    #         "gender",
    #         "password",
    #         "language",
    #         "currency",
    #         "superhost",
    #     )

    #     list_filter = (
    #         "superhost",
    #         "language",
    #         "currency",
    #     )

