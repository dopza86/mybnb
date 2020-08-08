from django.utils import timezone
import calendar


class Day:
    # 날짜를 표시하는 클래스
    def __init__(self, number, past, month, year):
        self.number = number
        self.past = past
        self.month = month
        self.year = year

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        # 요일별로 0~6으로 진행됨 , 6이면 일요일
        self.year = year
        self.month = month
        self.day_names = ("일", "월", "화", "수", "목", "금", "토")
        self.months = (
            "1월",
            "2월",
            "3월",
            "4월",
            "5월",
            "6월",
            "7월",
            "8월",
            "9월",
            "10월",
            "11월",
            "12월",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        # monthdays2calendar 한주의 요일과 날짜를 튜플 형식으로 출력
        days = []
        for week in weeks:
            for day, _ in week:
                # 튜플을 언패킹 한다 , _로 표시한 인자는 출력되지 않는다
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month == self.month:
                    # 실제의 달과 달력의 달을 비교한다
                    if day <= today:
                        # 달력의 날짜가 실제의 날자보다 이전일때
                        past = True
                new_day = Day(number=day, past=past, month=self.month, year=self.year)

                days.append(new_day)

        return days

    def get_month(self):
        return self.months[self.month - 1]
        # months 중에 어떤 달을 리턴할지 정한다
        # 커스터마이징을 하지않고 메서드를 사용하지 않고 month 그대로 출력해도 된다

