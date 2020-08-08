from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rooms import models as room_models
from users import mixins as user_mixins
from . import models

# Create your views here.
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            # 튜플을 언패킹한다
            user=request.user,
            name=f"{request.user}님의 관심 여행지",
            # 템플릿 태그에서도 같은 이름으로 작성해야한다
        )  # get_or_create 없을경우 새로 만든다
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
            # https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/ 에서 각종 기능 확인가능

    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(user_mixins.LoggedInOnlyView, TemplateView):
    template_name = "lists/list_detail.html"

    # 내가 가진 즐겨찾기 리스트는 단하나 이기 때문에 리스트뷰가 아닌 템플릿뷰로 템플릿에 바로 렌더링을 해준다
    # TemplateView는 템플릿을 렌더링합니다. URLconf에서 키워드 인수를 컨텍스트로 전달합니다.


# class TemplateView(TemplateResponseMixin, ContextMixin, View):
#     """
#     Render a template. Pass keyword arguments from the URLconf to the context.
#     """
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)
# 템플릿뷰는 이렇게 생겨먹었다 , kwargs를 템플릿에 전달해주는 역할을 한다


# 리스트뷰는 모델 자체 또는 쿼리셋의 객체목록을 랜더링하고 , 템플릿뷰는 단순히 현재 전달받은kwargs를 렌더링해 템플릿에 전달해준다

