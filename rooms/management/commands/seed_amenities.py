from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "편의 시설을 생성하는 커맨드 입니다"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you that I love you?"
    #     )

    #     # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):

        amenities = [
            "주방",
            "샴푸",
            "난방",
            "에어컨",
            "세탁기",
            "건조기",
            "무선 인터넷",
            "아침식사",
            "실내 벽난로",
            "옷걸이",
            "다리미",
            "헤어드라이어",
            "노트북 작업 공간",
            "TV",
            "아기 침대",
            "유아용 식탁의자",
            "셀프 체크인",
            "화재경보기",
            "일산화탄소 경보기",
            "욕실 단독 사용",
            "수변",
        ]

        for a in amenities:
            room_models.Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("편의 시설 생성!"))
