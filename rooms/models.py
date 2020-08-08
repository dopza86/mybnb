from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField
from core import models as core_models
from cal import Calendar


# from users import models as user_models , "users.User" 로 불러올경우 따로 임포트를 안해줘도 된다

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 방종류 ,편의시설 , 시설 등등에서 사용할것이기에 추상 아이템을 만들어준다


class RoomType(AbstractItem):
    class Meta:
        verbose_name_plural = "객실종류"
        ordering = ["name"]  # 각종 정렬기준을 넣을수 있는데 예를들어 -name 일 경우는 역순으로 정렬


class Amenity(AbstractItem):
    class Meta:
        verbose_name_plural = "편의시설"
        ordering = ["name"]


class Facility(AbstractItem):
    class Meta:
        verbose_name_plural = "시설"
        ordering = ["name"]


class HouseRule(AbstractItem):
    class Meta:
        verbose_name_plural = "이용규칙"
        ordering = ["name"]


class Photo(core_models.TimeStampedModel):
    """ 포토 모델 정의 """

    caption = models.CharField(verbose_name="설명", max_length=80)
    file = models.ImageField(
        verbose_name="파일", upload_to="room_photos", blank=True)
    room = models.ForeignKey(
        "Room", verbose_name="객실", related_name="photos", on_delete=models.CASCADE
    )
    # room = models.ForeignKey(Room, on_delete=models.CASCADE) 로 작성할경우 , 위에서 아래로 코드를 읽고 수행하기에
    # 룸 클래스를 제대로 가져오지 못한다

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "사진"
        verbose_name_plural = "사진"


class Room(core_models.TimeStampedModel):

    """ 룸 모델 정의 """

    name = models.CharField(verbose_name="이름", max_length=140)
    description = models.TextField(verbose_name="설명")
    country = CountryField(verbose_name="국가")
    city = models.CharField(verbose_name="도시", max_length=80)
    price = models.IntegerField(verbose_name="가격")
    address = models.CharField(verbose_name="주소", max_length=140)
    guests = models.IntegerField(verbose_name="숙박인원", default=0)
    beds = models.IntegerField(verbose_name="침대")
    bedrooms = models.IntegerField(verbose_name="침실")
    baths = models.IntegerField(verbose_name="욕실")
    check_in = models.TimeField(verbose_name="체크인 시간")
    check_out = models.TimeField(verbose_name="체크아웃 시간")
    instant_book = models.BooleanField(verbose_name="즉시예약", default=False)
    host = models.ForeignKey(
        "users.User", verbose_name="호스트", related_name="rooms", on_delete=models.CASCADE
    )  # 하나만 선택가능, related_name 을 설정함으로서 외래키가 가리키는 대상에서 역으로 호출을 할수있다
    # users.User 는 room_set 을 가지고 있어서 related_name 으로 역으로 사용가능하다
    room_type = models.ForeignKey(
        "RoomType", verbose_name="객실종류", related_name="rooms", on_delete=models.SET_NULL, null=True,
    )
    # ForeignKey가 바라보는값 이 삭제될때 필드의 값을 null 로 바꾼다
    amenities = models.ManyToManyField(
        "Amenity", verbose_name="편의시설", related_name="rooms", blank=True
    )
    facilities = models.ManyToManyField(
        "Facility", verbose_name="시설", related_name="rooms", blank=True
    )
    house_rules = models.ManyToManyField(
        "HouseRule", verbose_name="이용규칙", related_name="rooms", blank=True
    )

    # reservations = models.ForeignKey(
    #     "reservations.Reservation",
    #     verbose_name="예약상황",
    #     related_name="rooms",
    #     on_delete=models.CASCADE,
    #     null=True,
    # )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save()

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})
        # get_absolute_url 메소드로 디테일뷰에 pk 값을 전달해준다

    def total_rating(self):

        all_reviews = self.reviews.all()
        # related_name 으로 리뷰와 연결되어 있다 , 모든 리뷰들을 가져와라

        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
            # review.rating_average() ->review 에있는 rating_average함수 호출

        if all_ratings == 0:
            return 0

        else:
            return round(all_ratings / len(all_reviews), 2)

    total_rating.short_description = "평균점수"

    # 리뷰에 있는 모든 개인별 평정을 가지고 와서 총 평점을 구한다

    class Meta:
        verbose_name = "객실"
        verbose_name_plural = "객실"

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]

        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        next_year = this_year
        this_month = now.month
        next_month = this_month + 1
        str_this_month = str(this_month)
        if this_month == 12:
            next_month = 1
            next_year = this_year + 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(next_year, next_month)
        return [this_month_cal, next_month_cal]

        # 이미 만들어진 cal.py에 시간을 지정하여 템플릿에 전달해주는 방법을 정하는 메쏘드 이다
