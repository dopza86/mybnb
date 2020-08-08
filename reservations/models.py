import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models


# Create your models here.
class BookedDay(core_models.TimeStampedModel):
    # 예를들어 15~21일 까지 예약을 했을때 16~20일의 에약 상황을 알수없기에 그것을 알수있는 클래스를 생성한다
    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "예약일"
        verbose_name_plural = "예약일"


class Reservation(core_models.TimeStampedModel):

    """ 예약 모델 정의 """

    STATUS_PENDING = "진행중"
    STATUS_CONFIRMED = "확정"
    STATUS_CANCELED = "취소"

    STATUS_CHOICES = (
        (STATUS_PENDING, "진행중"),
        (STATUS_CONFIRMED, "확정"),
        (STATUS_CANCELED, "취소"),
    )

    status = models.CharField(
        verbose_name="상태", max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField(verbose_name="체크인")
    check_out = models.DateField(verbose_name="체크아웃")
    guest = models.ForeignKey("users.User", verbose_name="예약자", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", verbose_name="객실", related_name="reservation", on_delete=models.CASCADE
    )

    def __str__(self):

        return f"예약자 : {self.guest} - 객실 : {self.room} - 예약상태 : {self.status} - 체크인/체크아웃 : {self.check_in}/{self.check_out}"

    def host(self, *args, **kwargs):
        host = self.room.host
        print(host)
        return host

    host.short_description = "호스트"
    # foreignkey 로 가져온 모델의 객체를 표시할때 함수를 이용해보자

    def in_progress(self):
        now = timezone.now().date()

        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True
    in_progress.short_description = "숙박중"

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True
    is_finished.short_description = "숙박종료"

    def save(self, *args, **kwargs):
        # reservation 이 있어야지 BookedDay 가 외래키로 reservation을 받을수 있다 그러므로
        # 세이브를 가로채서 BookedDay를 생성해야한다
        if self.pk is None:
            # 예약 사항이 없다면
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(day__range=(start, end)).exists()
            # BookedDay 에 day가 있기때문에 day__range 를 쓸수있다
            # exists() 를 통해 존재여부를 확인할수있다

            if not existing_booked_day:
                super().save(*args, **kwargs)
                # reservation 이 있어야지 BookedDay 가 외래키로 reservation을 받을수 있다
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    # timedelta 시간사이의 간격을 계산할때 사용
                    BookedDay.objects.create(day=day, reservation=self)
                    # 예약일 부터 하루씩 예약을 생성한다
                return
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "예약"
        verbose_name_plural = "예약"

