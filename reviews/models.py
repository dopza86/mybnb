from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models

# Create your models here.


class Review(core_models.TimeStampedModel):

    """리뷰 모델 정의"""

    review = models.TextField(verbose_name="리뷰", blank=True, null=True)
    cleanliness = models.IntegerField(
        verbose_name="청결도", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    accuracy = models.IntegerField(
        verbose_name="정확성", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        verbose_name="의사소통", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        verbose_name="위치", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        verbose_name="체크인", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(
        verbose_name="가격 대비 만족도", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "users.User", verbose_name="리뷰 작성자", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", verbose_name="객실 이름", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"작성자 : {self.user} -- 리뷰 : {self.review} -- 객실정보: {self.room.host.username} 님의 {self.room}"
        # str(self.room.host.username) + "-" + str(self.room.name)

    def rating_average(self):

        avg = (
            self.cleanliness
            + self.accuracy
            + self.communication
            + self.location
            + self.check_in
            + self.value
        ) / 6

        return round(avg, 1)

    rating_average.short_description = "평점"

    class Meta:
        ordering = ("-created",)
        verbose_name = "후기"
        verbose_name_plural = "후기"
