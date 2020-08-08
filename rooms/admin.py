from django.contrib import admin
from django.utils.html import mark_safe
from django.http import HttpResponse

from . import models


# Register your models here.
@admin.register(models.RoomType, models.Amenity, models.Facility,
                models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """아이템 어드민 정의"""

    list_display = ("name", "used_by")

    def used_by(self, obj):

        return obj.rooms.count()

    used_by.short_description = "사용중인 객실"


class PhotoInline(admin.TabularInline):  # StackedInline 도 있다
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """룸 어드민 정의"""

    inlines = (PhotoInline, )

    fieldsets = (
        (
            "기본정보",
            {
                "fields":
                ("name", "description", "country", "city", "address", "price")
            },
        ),
        (
            "시간",
            {
                "fields": ("check_in", "check_out", "instant_book")
            },
        ),
        (
            "이용정보",
            {
                "classes": ("collapse", ),
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                )
            },
        ),
        # 클래스를 추가함으로서 옵션을 추가할수 있다
        (
            "객실정보",
            {
                "fields": (
                    "beds",
                    "bedrooms",
                    "baths",
                    "guests",
                )
            },
        ),
        (
            "호스트",
            {
                "fields": ("host", )
            },
        ),
        # ("예약상황", {"fields": ("reservations",)},),
    )
    actions = ['download_csv']

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_type",
        "count_amenities",
        "count_photos",
        "total_rating",
        # "reservations",
    )

    def download_csv(self, request, queryset):
        import csv
        f = open('some.csv', 'w')
        writer = csv.writer(f)
        writer.writerow([
            "name",
            "country",
            "city",
            "price",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "host",
            "room_type",
        ])
        for s in queryset:
            writer.writerow([
                s.name,
                s.country,
                s.city,
                s.price,
                s.guests,
                s.beds,
                s.bedrooms,
                s.baths,
                s.check_in,
                s.check_out,
                s.instant_book,
                s.host,
                s.room_type,
            ])
        f.close()
        f = open('some.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=room_admin.csv'
        return response

    download_csv.short_description = "csv 로 다운로드"

    ordering = ("id", )
    # 모델의 정렬 순서를 지정하며 여러 개를 지정할 경우 필드 이름을 리스트로 나열한다.
    # 기본값은 오름차순으로 정렬하고 -를 붙이면 내림차순으로 정렬한다.

    # 다대다 필드는 리스트 디스플레이에 추가 불가

    list_filter = (
        "instant_book",
        "host__superhost",
        "city",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    raw_id_fields = ("host", )

    search_fields = ("city", "host__username")
    # "host__username" 외래키로 가져온 호스트의 유저네임 속성으로 검색을 한다
    # 유저 모델을 보면 유저네임이 작성되어있지 않은데 이는 abstractuser를 상속받아 오버라이딩해 사용하기에 해당속성을 기본으로 가지고 있다
    # 기본적으로 대소문자 구분없이 검색가능
    # 검색단위 앞에 아래 옵션을 붙일수 있다
    # ^	startswith
    # =	iexact
    # @	search
    # None	icontains

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # 다대다 관계에서 작동한다

    def save_model(self, request, obj, form, change):
        print(obj, change, form)
        super().save_model(request, obj, form, change)

    # 저장할때마다 로그를 기록한다

    def count_amenities(self, obj):  # 모델에서 정의된 필드가 아니라서 어드민에서 클릭이 안된다
        # self 는 현재의 룸 어드민 그자체
        # obj 는 생성된 객실들
        # print(obj.amenities.all().count())

        return str(obj.amenities.all().count())

    count_amenities.short_description = "시설 갯수"

    # short_description 으로 어드민에서 표시되는 column 을 바꿔준다

    def count_photos(self, obj):

        return str(obj.photos.count())
        # 포토 모델 클래스에 related_name 이 설정되어 있어서 가져와서 쓸수있다

    count_photos.short_description = "사진 갯수"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """포토 어드민 정의"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):

        return mark_safe(f"<img width=50px src='{obj.file.url}'/>")
        # from django.utils.html import mark_safe

    get_thumbnail.short_description = "미리보기"
