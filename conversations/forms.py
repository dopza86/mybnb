from django import forms


class AddCommentForm(forms.Form):

    message = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "메세지를 입력하세요"})
    )


#  <form class="mt-10 w-1/2 mx-auto" method="POST">
#                 {% csrf_token %}
#                 <input class="border-box mb-5" name="message" placeholder="메세지를 입력하세요" required />
#                 <button class="btn-link">메세지 보내기</button>
#             </form>
#  이렇게 했기 때문에 뷰에서 폼을 전달해주지 않았다
# 템플릿에서 인풋을 사용했으며 폼을 사용치 않았다 , 이런식으로도 사용을 할수있다
