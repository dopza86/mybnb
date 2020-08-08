import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return

    try:

        date = datetime.datetime(
            year=day.year, month=day.month, day=day.number)
        # 템플릿에서 day를 가져올수 있으며 day 의 BookedDay를 얻을수있다
        reservation_models.BookedDay.objects.get(
            day=date, reservation__room=room)
        # 날짜의 예약이 있는 방을 가져온다
        return True

    except reservation_models.BookedDay.DoesNotExist:
        return False
