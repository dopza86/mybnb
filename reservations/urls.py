from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path("create/<int:room_pk>/<int:year>-<int:month>-<int:day>", views.create, name="create"),
    # 템플릿에서 전달받은 값들이 순서대로 들어간다
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>", views.edit_reservation, name="edit"),
]
