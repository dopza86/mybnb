from django.db import models
from core import models as core_models

# Create your models here.


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField(
        "users.User", verbose_name="참여자", related_name="conversation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
            print(self.participants.all())

        return " // ".join(usernames)  # 코어모델에서 상속받은 내용 메시지가 만들어진 시간

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "메시지 갯수"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "참여자 수"

    class Meta:
        verbose_name = "대화"
        verbose_name_plural = "대화"


class Message(core_models.TimeStampedModel):

    message = models.TextField()
    user = models.ForeignKey("users.User", related_name="messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"

    class Meta:
        verbose_name = "메세지"
        verbose_name_plural = "메세지"

