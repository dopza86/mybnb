from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from users import models as user_models
from . import models, forms


def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            # conversation 을 일단 생성
            conversation.participants.add(user_one, user_two)
            # 유저를 추가

        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))
        # conversation = models.Conversation.objects.filter(participants=user_one).filter(participants=user_two)
        # 필터를 두번씩 사용하면 db 에 좋을리가 없다 , 복잡한 쿼리들은 q 오브젝트를 통해 다루도록 하자


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404("페이지를 찾을 수 없습니다")
        return render(
            self.request, "conversations/conversation_detail.html", {"conversation": conversation},
        )
        # 템플릿에 conversation context를 전달한다

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404("페이지를 찾을 수 없습니다")
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))

