from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(label="도시", initial="장소를 입력 하세요", required=False)
    country = CountryField(default="KR").formfield(label="국가")
    price = forms.IntegerField(label="가격", required=False)
    room_type = forms.ModelChoiceField(
        required=False,
        label="객실종류",
        empty_label="객실을 선택 하세요",
        queryset=models.RoomType.objects.all(),
    )
    guests = forms.IntegerField(label="숙박인원", required=False)  # help_text="숙박 인원의 수를 입력하세요",
    beds = forms.IntegerField(label="침대갯수", required=False)
    bedrooms = forms.IntegerField(label="침실수", required=False)
    baths = forms.IntegerField(label="욕실수", required=False)
    instant_book = forms.BooleanField(label="즉시예약", required=False)
    superhost = forms.BooleanField(label="슈퍼호스트", required=False)
    amenities = forms.ModelMultipleChoiceField(
        label="편의시설",
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        label="시설",
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    print(amenities)

    def clean(self):
        amenities = self.cleaned_data.get("amenities")
        print(self.cleaned_data)
        return self.cleaned_data


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):

        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()
        # form 에게 오브젝트를 생성하라는 뜻이기도 하다
        # room 객체의 pk 가 필요한데 form 에서는 받아올 방법이 없다 , 뷰에서 form_valid 를 통해 받아오도록 한다


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
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

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        # 룸을 생성만함 (유저는 없음)
        return room
        # 그리고 리턴 => view 에서 처리
