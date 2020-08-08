import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "리뷰를 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="생성 하고싶은 리뷰의 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(
            review_models.Review,
            number,
            {
                "cleanliness": lambda x: random.randint(0, 5),
                "accuracy": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "check_in": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        # add_entity(모델, 갯수, {조건}) ,entity:개체
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number}개의 리뷰 생성!"))
