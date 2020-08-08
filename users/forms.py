from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(label="이메일", widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀립니다"))

        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("존재하지 않는 사용자입니다"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("last_name", "first_name", "email")
        widgets = {
            "last_name": forms.TextInput(attrs={"placeholder": "성"}),
            "first_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "email": forms.EmailInput(attrs={"placeholder": "이메일"}),
        }

    password = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )
    password1 = forms.CharField(
        label="비밀번호 확인", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 존재하는 사용자 입니다", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호가 서로 일치하지 않습니다")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        # commit=False를 하게 되면 데이터베이스에 당장 저장하지 않는다.
        # 언제쓰지? : DB에 데이터를 저장하기 전에 특정 행위를 하고 싶을 때 사용한다
        # 저장을 늦게 시켜서 사용자가 원하는 추가적인 정보를 저장할 수 있는 것이라고 생각하면 된다
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
