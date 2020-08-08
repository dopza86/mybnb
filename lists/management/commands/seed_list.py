import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = " 목록을 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="생성 하고싶은 목록의 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users),},
        )
        # add_entity(모델, 갯수, {조건}) ,entity:개체
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        # 생성된 리스트의 pk 값을 가져 올수 있다

        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            random_room = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*random_room)
            # *이 붙은 이유는 배열안의 요소들을 전부 집어넣기 위함이다

        self.stdout.write(self.style.SUCCESS(f"{number}개의 리스트 생성!"))
