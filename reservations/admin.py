from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """예약 어드민 정의"""

    list_display = (
        "room",
        "host",
        "guest",
        "status",
        "check_in",
        "check_out",
        "in_progress",
        "is_finished",
    )
    raw_id_fields = ("room",)
    list_filter = ("status",)

    search_fields = ("status", "room__name", "guest__username")


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    list_display = ("day", "reservation")
