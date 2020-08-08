from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    # 리스트는 유저가 가진 리스트인데 유저는 context 에서 가져와야한다
    the_list = list_models.List.objects.get_or_none(user=user, name=f"{user}님의 관심 여행지")

    if the_list is not None:
        # 만약 리스트가 존재하지 않는다면 어떠한 값도 리턴하지 못해서 논타입 에러가 발생한다
        # 따라서 리스트가 존재 할때를 이프문으로 추가해줘야한다
        return room in the_list.rooms.all()
    return False
    # 룸이 리스트 안에 있는지 여부를 boolean 값으로 리턴한다


# 데코레이터의 takes_context=True로 설정해주면,
# 부모 템플릿의 context의 값을 가져와 호출하는 템플릿으로 전달할 수 있습니다.

