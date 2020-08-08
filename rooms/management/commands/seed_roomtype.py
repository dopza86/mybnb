from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "시설을 생성하는 커맨드 입니다"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you that I love you?"
    #     )

    #     # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):

        room_type = [
            "주택",
            "아파트",
            "B&B",
            "부티크 호텔",
            "게스트 스위트",
            "게스트용 별채",
            "레지던스",
            "로프트",
            "리조트",
            "방갈로",
            "샬레",
            "저택",
            "전원주택",
            "타운하우스",
            "통나무집",
            "호스텔",
            "호텔",
        ]

        for r in room_type:
            room_models.RoomType.objects.create(name=r)
        self.stdout.write(self.style.SUCCESS("객실 종류 생성!"))
