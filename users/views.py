import os
import requests
from django.utils import translation
from django.http import HttpResponse
from django.conf import settings

# import google.oauth2.credentials
# import google_auth_oauthlib.flow
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from . import forms, models, mixins

# Create your views here.


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    # success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        # authenticate =>주어진 자격 증명이 유효하면 User 객체를 반환합니다.
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
        # return super().form_valid(form) 의 기능은
        # form_valid 함수를 통해서 cleaned_data 관련 로직을 수행하고 성공적으로 마치면
        # 알아서 success_url에서 정의한 페이지로 폼과 함께 이동해준다

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next is not None:
            return next_arg
        # 로그인 되지 않은 상태에서 LoggedInOnlyView 에 접근하면 나오는 페이지에서 다시 로그인을 하면
        # next_arg 로 계속 진행
        else:
            return reverse("core:home")


def log_out(request):

    messages.info(request, f"{request.user.username}님 이용해 주셔서 감사합니다")
    logout(request)

    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        # authenticate =>주어진 자격 증명이 유효하면 User 객체를 반환합니다.
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # 성공 메시지 추가할것
    except models.User.DoesNotExist:
        # 에러 메시지 추가할것
        pass
    return redirect(reverse("core:home"))


# 유저들은 깃허브 아이덴티티를 요청하기위해 깃허브로 리다이렉트 된다
# 유저들을 깃허브에 의해 다시 웹사이트로 리다이렉트 된다
# 유저의 억세스 토큰으로 유저의 정보 api를 받을수 있다 (토큰은 깃허브의 코드와 교환한다 ,그걸 교환하는 함수가 콜백함수)
# 깃허브 콜백 함수를 통해 우리사이트에 로그인 시킨다
# https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/ 참조


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://https://mybnbbnb.herokuapp.com//users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
                # requests 라이브러리를 이용해서 코드와 토큰을 교환해 json을 받아온다
                # HTTP 헤더는 클라이언트와 서버가 요청 또는 응답으로 부가적인 정보를 전송할 수 있도록 해줍니다
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            # json 의 에러를 체크한다

            if error is not None:
                # 에러가 있다면
                raise GithubException("토큰에 접근할 수 없습니다")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                # access_token을 통해 api를 받아온다
                profile_json = profile_request.json()
                # profile_json 을 받아온다
                username = profile_json.get("login", None)

                if username is not None:
                    name = profile_json.get("login")

                    try:
                        user = models.User.objects.get(username=name)
                        if user.login_method == models.User.LOGIN_EMAIL:
                            raise GithubException(
                                f"이미 가입된 회원입니다 이메일과 비밀번호 입력을 통해 로그인을 해주세요 ")
                        if user.login_method == models.User.LOGIN_KAKAO:
                            raise GithubException(
                                f"이미 가입된 회원입니다 카카오로 로그인을 해주세요 ")
                        if user.login_method == models.User.LOGIN_GOOGLE:
                            raise GithubException(
                                f"이미 가입된 회원입니다 구글로 로그인을 해주세요 ")

                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=name,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"{user.username} 님 반갑습니다")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("프로필을 불러올수 없습니다")
        else:
            raise GithubException("인증코드를 받을수없습니다")

    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    app_key = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://https://mybnbbnb.herokuapp.com//users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        app_key = os.environ.get("KAKAO_KEY")
        code = request.GET.get("code")
        redirect_uri = "http://https://mybnbbnb.herokuapp.com//users/login/kakao/callback"
        post_data = {
            "grant_type": "authorization_code",
            "client_id": app_key,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        token_request = requests.post(f"https://kauth.kakao.com/oauth/token",
                                      data=post_data)
        token_json = token_request.json()
        error = token_json.get("error", None)

        if error is not None:
            raise KakaoException("인증코드를 받을수 없습니다")
        else:
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            profile_json = profile_request.json()

            kakao_account = profile_json.get("kakao_account")
            properties = profile_json.get("properties")
            profile = kakao_account.get("profile")
            email = kakao_account.get("email", None)
            if email is None:
                raise KakaoException("이메일 주소를 입력 바랍니다")
            nickname = properties.get("nickname")
            profile_image = properties.get("profile_image")

            try:
                user = models.User.objects.get(username=nickname)
                if user.login_method == models.User.LOGIN_EMAIL:
                    raise KakaoException(
                        f"이미 가입된 회원입니다 이메일과 비밀번호 입력을 통해 로그인을 해주세요 ")
                if user.login_method == models.User.LOGIN_GITHUB:
                    raise KakaoException(f"이미 가입된 회원입니다 깃허브로 로그인을 해주세요 ")
                if user.login_method == models.User.LOGIN_GOOGLE:
                    raise KakaoException(f"이미 가입된 회원입니다 구글로 로그인을 해주세요 ")
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    username=nickname,
                    email=email,
                    login_method=models.User.LOGIN_KAKAO,
                )
                user.set_unusable_password()
                user.save()

                if profile_image is not None:
                    photo_request = requests.get(profile_image)

                    user.avatar.save(f"{nickname}-사진",
                                     ContentFile(photo_request.content))
            login(request, user)
            messages.success(request, f"{user.username} 님 반갑습니다")
            return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def google_login(reguest):
    client_id = os.environ.get("GOOGLE_ID")
    redirect_uri = "http://https://mybnbbnb.herokuapp.com//users/login/google/callback"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email&access_type=offline"
    )


class GoogleException(Exception):
    pass


def google_callback(request):
    try:
        client_id = os.environ.get("GOOGLE_ID")
        client_secret = os.environ.get("GOOGLE_SECRET")
        code = request.GET.get("code")
        redirect_uri = "http://https://mybnbbnb.herokuapp.com//users/login/google/callback"
        post_data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        token_request = requests.post(f"https://oauth2.googleapis.com/token",
                                      data=post_data)
        token_json = token_request.json()
        print(token_json)

        error = token_json.get("error", None)
        if error is not None:
            raise GoogleException("인증코드를 받을수 없습니다")
        else:
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                f"https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            email = profile_json.get("email", None)
            profile_image = profile_json.get("picture")
            if email is None:
                raise GoogleException("이메일 주소를 입력 바랍니다")
            try:
                user = models.User.objects.get(email=email)

                if user.login_method != models.User.LOGIN_GOOGLE:
                    if user.login_method == models.User.LOGIN_EMAIL:
                        raise GoogleException(
                            f"이미 가입된 회원입니다 이메일과 비밀번호 입력을 통해 로그인을 해주세요 ")
                    if user.login_method == models.User.LOGIN_GITHUB:
                        raise GoogleException(f"이미 가입된 회원입니다 깃허브로 로그인을 해주세요 ")
                    if user.login_method == models.User.LOGIN_KAKAO:
                        raise GoogleException(f"이미 가입된 회원입니다 카카오로 로그인을 해주세요 ")

            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    username=email,
                    email=email,
                    login_method=models.User.LOGIN_GOOGLE,
                    email_verified=True,
                )
                user.set_unusable_password()
                user.save()

                if profile_image is not None:
                    photo_request = requests.get(profile_image)

                    user.avatar.save(f"{email}-사진",
                                     ContentFile(photo_request.content))
            login(request, user)
            messages.success(request, f"{user.username} 님 반갑습니다")
            return redirect(reverse("core:home"))

    except GoogleException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"

    # user_obj 는 현재 로그인한 유저

    # def def get_context_data(self, **kwargs):
    #     # 더많은 컨텍스트들을 확장 가능하다
    #     context = super(ViewName, self).get_context_data(**kwargs)
    #     context["something"] = "something"
    #     #something 이라는 컨텍스트의 확장이 가능해진다

    #     return context


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin,
                        UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    success_message = "프로필이 변경되었습니다"

    def get_object(self, queryset=None):

        return self.request.user
        # 우리가 수정하길 원하는값을 반환한다 기본값은 pk 또는 slug 이다

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["last_name"].widget.attrs = {"placeholder": "성"}
        form.fields["first_name"].widget.attrs = {"placeholder": "이름"}
        form.fields["bio"].widget.attrs = {"placeholder": "설명"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "생일"}
        return form

    # def form_valid(self,form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super.form_valid(form)
    # 폼뷰 사용시  입력한 이메일을 유저네임으로 변경하는 메쏘드


class UpdatePasswowdView(mixins.LoggedInOnlyView, mixins.EmailLoginOnlyView,
                         PasswordChangeView):

    template_name = "users/update-password.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "현재 비밀번호"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "새로운 비밀번호"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "새로운 비밀번호 확인"
        }
        return form
        # form.fields["old_password"].label = "이전 비밀번호"
        # form.fields["new_password1"].label = "새로운 비밀번호"
        # form.fields["new_password2"].label = "새로운 비밀번호 확인"
        # https://velog.io/@ggg/PasswordChangeForm-Issue-about-labelsuffix 를 참조해서 label 을 변경하였다

    def get_success_url(self):
        return self.request.user.get_absolute_url()
        # get_absolute_url 을 통해 비밀번호 변경이 완료 되면 해당 페이지로 리턴된다


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
        # is_hosting 키값이 있다면 세션에서 삭제
    except KeyError:
        # is_hosting 키값이 없다면
        request.session["is_hosting"] = True
        # 세션에 추가한다
    return redirect(reverse("core:home"))


# httpSession's setAttribute("Key", Value)
# "Key"를 사용하여 객체를 세션에 바인딩한다.
# Value는 값으로 들어올 자료형을 예측할 수 없기에 Object형으로 업캐스팅하여 모두 받아낸다.
# HttpSession's getAttribute("Key")
# "Key"로 바인딩된 객체를 돌려주고, "Key"로 바인딩된 객체가 없다면 null를 돌려준다.
# Value는 세션을 저장할 때 Object형으로 업캐스팅을 했으므로, 가져올 땐 원래대로 다운캐스팅 해야 한다.
# HttpServletRequest's getSession(true)
# 이미 세션이 있다면 그 세션을 돌려주고, 세션이 없으면 새로운 세션을 생성한다.
# request.getSession()로 쓸 수 있다.
# HttpServletRequest's getSession(false)
# 이미 세션이 있다면 그 세션을 돌려주고, 세션이 없으면 null을 돌려준다.


def switch_language(request):
    lang = request.GET.get("lang", None)
    translation.activate(lang)
    response = HttpResponse(status=200)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
