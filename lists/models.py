from django.db import models
from core import models as core_models

# Create your models here.
class List(core_models.TimeStampedModel):

    """ 리스트 모델 정의 """

    name = models.CharField(verbose_name="이름", max_length=80)
    user = models.OneToOneField(
        "users.User", verbose_name="유저이름", related_name="lists", on_delete=models.CASCADE
    )  # 오직 하나의 리스트만 가져야 하니까 일대일 필드를 생성
    rooms = models.ManyToManyField(
        "rooms.Room", verbose_name="객실명", related_name="lists", blank=True
    )

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "방갯수"

    class Meta:
        verbose_name = "목록"
        verbose_name_plural = "목록"

