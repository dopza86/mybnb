from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """리뷰어드민 정의"""

    list_display = ("__str__", "rating_average")

    pass
