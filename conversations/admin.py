from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """메시지 어드민 정의"""

    list_display = ("__str__", "created")


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "count_participants",
        "count_messages",
    )

    pass
