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

        facilities = [
            "건물 내 무료 주차",
            "헬스장",
            "자쿠지",
            "수영장",
        ]

        for f in facilities:
            room_models.Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("시설 생성!"))
