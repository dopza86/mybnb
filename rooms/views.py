from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django_countries import countries
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):

    """홈뷰의 정의"""

    # http://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/ 참조

    # 템플릿 네임을 지정하지 않을경우 장고 어드민에서 시키는대로 지정을 해줘도 된다
    model = models.Room
    paginate_by = 12
    paginate_orphans = 6
    ordering = "created"
    page_kwarg = "page"
    context_object_name = "rooms"


# def room_detail(request, pk):

#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()


class RoomDetail(DetailView):

    """ 룸 자세히 보기 정의 """

    model = models.Room


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "장소를 입력 하세요":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity
                    # cleaned_data 를 거쳐서 오기때문에 __pk 로 필터링을 할 필요가 없다

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("created")
                paginator = Paginator(qs, 5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                query_string = request.environ.get("QUERY_STRING")
                # 쿼리스트링을 활용해서 입력된 주소를 기억할수 있다

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms, "query_string": query_string},
                )

            # request.GET 으로 무엇을 입력했는지 기억 한다
        else:
            form = forms.SearchForm()
            # 처음 페이지를 열었을때 폼을 받아오는 부분

            return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        # 현재 보고있는 룸을 찾는다
        if room.host.pk != self.request.user.pk:
            # 룸 호스트의 pk 와 접속한 유저의 pk를 비교한다
            raise Http404("페이지를 찾을수 없습니다")
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):

        room = super().get_object(queryset=queryset)

        if room.host.pk != self.request.user.pk:
            raise Http404("페이지를 찾을수 없습니다")
        return room


@login_required
# 로그인 하지 않을경우 setting.LOGIN_URL 로 이동
# fbv 이기 때문에 데코레이터 사용 , cbv 일때는 믹스인 상속
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "사진을 삭제할 수 없습니다")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "사진을 삭제 하였습니다")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))

    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    # 업데이트뷰는 pk값만을 찾기에 따로 지정을 해줘야한다

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    # pk 말고 photo_pk 를 찾아라
    success_message = "사진 업데이트 성공"
    fields = ("caption",)

    def get_success_url(self):
        # 수정 성공시 돌아갈 url
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotosView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "rooms/photo_create.html"

    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        user_pk = self.request.user.pk
        room = models.Room.objects.get(pk=pk)
        host_pk = room.host.pk
        if host_pk != user_pk:
            raise Http404("페이지를 찾을수 없습니다")
        else:
            form.save(pk)
        # form에 room의 pk 값을 전달해준다
        messages.success(self.request, "사진이 업로드 되었습니다")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        # 폼에서 생성된 룸을 저장
        room.host = self.request.user
        # 룸의 호스트는 현재 작성자
        room.save()
        # 룸 저장
        form.save_m2m()
        # 다대다 필드 저장=>  m2m 필드를 저장할때 데이터베이스에 저장한후에 사용가능하다
        messages.success(self.request, "객실이 등록 되었습니다")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


@login_required
def delete_room(request, pk):
    user = request.user

    try:
        room = models.Room.objects.get(pk=pk)
        if room.host.pk != user.pk:
            messages.error(request, "객실을 삭제할 수 없습니다")
        else:
            room.delete()
            messages.success(request, "객실을 삭제 하였습니다")
        return redirect(reverse("core:home"))
    except room.DoesNotExist:
        return redirect(reverse("core:home"))

