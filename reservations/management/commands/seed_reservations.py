import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = " 예약을 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="생성 하고싶은 목록의 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["진행중", "확정", "취소"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now() + timedelta(days=random.randint(1, 20)),
            },
        )
        # add_entity(모델, 갯수, {조건}) ,entity:개체

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number}개의 예약이 생성되었습니다"))
