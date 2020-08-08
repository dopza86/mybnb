from django.db import models
from . import managers

# Create your models here.


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(verbose_name="생성 일시", auto_now_add=True)  # 모델을 생성할때마다 기록
    updated = models.DateTimeField(
        verbose_name="추가 일시", auto_now=True
    )  # 모델을 세이브할때마다 date,time 을 기록
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True  # abstract모델 즉 추상화를 시키면 데이터 베이스에 등록이 되지 않는다,오직 코드에서만 쓰임
