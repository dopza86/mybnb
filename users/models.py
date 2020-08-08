import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from core import managers as core_managers


# Create your models here.
class User(AbstractUser):  # 장고에서 제공해주는 유저모델을 상속받고 오버라이딩해서 사용

    """커스텀 유저 모델"""

    GENDER_MALE = "남자"
    GENDER_FEMALE = "여자"
    GENDER_OTHER = "기타"

    GENDER_CHOICES = (
        (GENDER_MALE, _("남자")),
        (GENDER_FEMALE, _("여자")),
        (GENDER_OTHER, _("기타")),
    )

    LANGUAGE_KOREAN = "ko"
    LANGUAGE_ENGLISH = "en"
    LANGUAGE_CHINESE = "cn"

    LANGUAGE_CHOICES = (
        (LANGUAGE_KOREAN, _("한국어")),
        (LANGUAGE_ENGLISH, _("english")),
        (LANGUAGE_CHINESE, _("汉语")),
    )

    CURRENCY_KRW = "krw"
    CURRENCY_USD = "usd"
    CURRENCY_RMB = "rmb"

    CURRENCY_CHOICES = (
        (CURRENCY_KRW, "krw"),
        (CURRENCY_USD, "usd"),
        (CURRENCY_RMB, "rmb"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_GOOGLE = "google"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "이메일"),
        (LOGIN_GITHUB, "깃허브"),
        (LOGIN_KAKAO, "카카오"),
        (LOGIN_GOOGLE, "구글"),
    )
    first_name = models.CharField(verbose_name="이름", max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name="성", max_length=50, blank=True, null=True)
    avatar = models.ImageField(verbose_name="사진", upload_to="avatars", blank=True)
    # null은 db 에 적용되는 값이고 blank는 form(양식)에 적용된다
    gender = models.CharField(_("gender"), choices=GENDER_CHOICES, max_length=16, blank=True)
    bio = models.TextField(_("bio"), default="", blank=True)
    birthdate = models.DateField(_("birthdate"), blank=True, null=True)
    language = models.CharField(
        _("language"), choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        verbose_name="사용화폐",
        choices=CURRENCY_CHOICES,
        max_length=3,
        blank=True,
        default=CURRENCY_KRW,
    )
    superhost = models.BooleanField(verbose_name="슈퍼호스트", default=False)
    email_verified = models.BooleanField(verbose_name="메일인증", default=False)
    email_secret = models.CharField(verbose_name="메일인증키", max_length=20, default="", blank=True)
    login_method = models.CharField(
        verbose_name="로그인 방법", max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    objects = core_managers.CustomUserManager()

    email = models.EmailField(verbose_name="이메일", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
        # get_absolute_url 메소드로 디테일뷰에 pk 값을 전달해준다

    def verify_email(self):

        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html", {"secret": secret})
            # html 을 스트링으로 바꾼다
            send_mail(
                _("마이비앤비 가입 인증메일 입니다"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()

        return

    def room_count(self):

        room_count = self.rooms.count()
        return room_count

    room_count.short_description = "운영중인 객실수"

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"
