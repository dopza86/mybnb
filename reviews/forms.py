from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    accuracy = forms.IntegerField(label="정확성", max_value=5, min_value=1)
    communication = forms.IntegerField(label="의사소통", max_value=5, min_value=1)
    cleanliness = forms.IntegerField(label="청결도", max_value=5, min_value=1)
    location = forms.IntegerField(label="위치", max_value=5, min_value=1)
    check_in = forms.IntegerField(label="체크인", max_value=5, min_value=1)
    value = forms.IntegerField(label="가격 대비 만족도", max_value=5, min_value=1)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(commit=False)
        return review

