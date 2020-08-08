from django.urls import path
from . import views


app_name = "reviews"

urlpatterns = [path("create/<int:room>", views.create_review, name="create")]
# 템플릿에서  reservation.room.pk  를 인자로 전달 받는다
