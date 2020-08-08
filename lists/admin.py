from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    """ 리스트 어드민 정의 """

    list_display = ("name", "user", "count_rooms")
    search_fields = (
        "name",
        "user__username",
    )

    filter_horizontal = ("rooms",)
