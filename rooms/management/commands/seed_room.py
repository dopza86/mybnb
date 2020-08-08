import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "객실을 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="생성 하고싶은 객실의 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randrange(10000, 200000, 10000),
                "guests": lambda x: random.randint(1, 5),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        # add_entity(모델,갯수,{조건})

        created_rooms = seeder.execute()
        # 이렇게 해놔도 seeder.execute() 가 실행된다
        created_clean = flatten(list(created_rooms.values()))
        # flatten 다차원 배열을 1차원으로 바꿔준다
        # 생성된 객실의 pk값을 받을수 있다
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        for pk in created_clean:  # 생성된 객실의 숫자만큼 반복문 실행
            room = room_models.Room.objects.get(pk=pk)  # 사진을 연결한 room

            """ 생성된 객실에 사진을 추가 해주는 반복문 """
            # 모델의 포토에 room 이 외래키로 연결 되어 있다
            for i in range(1, random.randint(3, 6)):  # 1번에서 3~6번 사이로 실행
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            """ 생성된 객실에 시설을 추가 해주는 반복문 """
            # 다대다 필드의 관계일때 랜덤으로 추가를 해주는 방법
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for h in house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(h)

        self.stdout.write(self.style.SUCCESS(f"{number} 개의 객실 생성!"))
