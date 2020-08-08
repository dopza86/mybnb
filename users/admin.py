from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.http import HttpResponse

from . import models
from rooms.models import Room

# Register your models here.


class RoomInline(admin.TabularInline):
    model = Room
    classes = ["collapse"]


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    inlines = (RoomInline, )

    fieldsets = UserAdmin.fieldsets + ((
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
    ), )

    list_filter = UserAdmin.list_filter + ("superhost", )

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

    actions = ['download_csv']

    def download_csv(self, request, queryset):
        import csv
        f = open('some.csv', 'w')
        writer = csv.writer(f)
        writer.writerow([
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
        ])
        for s in queryset:
            writer.writerow([
                s.username,
                s.login_method,
                s.date_joined,
                s.email_verified,
                s.email_secret,
                s.email,
                s.is_active,
                s.language,
                s.currency,
                s.superhost,
                s.is_staff,
                s.room_count,
            ])
        f.close()
        f = open('some.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=user_admin.csv'
        return response

    download_csv.short_description = "csv 로 다운로드"

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
