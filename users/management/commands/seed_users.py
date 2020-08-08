from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models


class Command(BaseCommand):

    help = "유저를 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help="생성 하고싶은 유저의 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        seeder.add_entity(user_models.User, number, {"is_staff": False, "is_superuser": False})
        # add_entity(모델, 갯수, {조건}) ,entity:개체
        seeder.execute()

        self.stdout.write(self.style.SUCCESS("유저 생성!"))
