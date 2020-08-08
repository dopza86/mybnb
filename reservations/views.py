import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from rooms import models as room_models
from users import mixins
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


@login_required
def create(request, room_pk, year, month, day):
    # room_pk, year, month, day 는 템플릿에서 전달받음
    # 나중에 createview 를 이용해 생성해보자
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room_pk)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        # 먼저 예약일과 방이 있는지 찾아본다

    except room_models.Room.DoesNotExist:
        messages.error(request, "객실이 존재하지 않습니다")
        return redirect(reverse("core:home"))

    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
            # 안타깝지만 장고만으로는 예약을 이렇게 밖에 못만든다 , 나중에 react 배워서 다시하자
        )

        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(mixins.LoggedInOnlyView, View):
    def get(self, *args, **kwargs):

        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user and reservation.room.host != self.request.user
        ):  # 예약한 게스트가 접속한 유저가 아니고 호스트도 아니면
            raise Http404("페이지를 찾을수 없습니다")
        form = review_forms.CreateReviewForm()
        # 예약이 확정되고 숙박이 종료되면 리뷰를 작성할수있게 폼을 넘겨준다

        return render(
            self.request, "reservations/detail.html", {"reservation": reservation, "form": form}
        )


# @login_required
# def get(request, *args, **kwargs):
#     pk = kwargs.get("pk")
#     reservation = models.Reservation.objects.get_or_none(pk=pk)
#     if not reservation or (
#         reservation.guest != request.user and reservation.room.host != request.user
#     ):
#         raise Http404("페이지를 찾을수 없습니다")
#     form = review_forms.CreateReviewForm()
#     return render(request, "reservations/detail.html", {"reservation": reservation, "form": form})
# 이런식으로 FBV 로 작성해도 된다


@login_required
# cbv 는 믹스인 fbv은 데코레이터!! 잘 써먹자
def edit_reservation(request, pk, verb):
    # 템플릿에서 pk, verb 를 전달받는다
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    # 매니저를 사용함으로서 존재하는지 여부를 간단하게 표시가능
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404("페이지를 찾을수 없습니다")
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    if verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
        messages.success(request, "예약을 취소 하였습니다")
        reservation.save()
        return redirect(reverse("rooms:detail", kwargs={"pk": reservation.pk}))
        # 예약을 삭제하면 예약일도 지워야한다

    reservation.save()
    messages.success(request, "예약을 업데이트 하였습니다")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))

