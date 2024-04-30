import reflex as rx
from app.app_state import AppState
import datetime
import calendar

cal = calendar.Calendar()


# class_State 분리
class State(rx.State):
    year: int = datetime.datetime.now().year
    month: int = datetime.datetime.now().month

    calendar_data: list[list[str]]

    # 날짜 선택
    selected_date: str | None = None  # Add to track selected date

    _on_change = None

    #
    def select_date(self, date: str) -> None:
        self.selected_date = date
        if self._on_change:
            self._on_change(date)
        self.get_calendar_data()

    # define a method to clear calendar data
    def clear_calendar_grid(self):
        self.calendar_data = []

    # define a method to populate the grid
    def get_calendar_data(self):
        self.clear_calendar_grid()
        print(self.selected_date)
        for week in cal.monthdayscalendar(self.year, self.month):
            temp_list: list = []
            for day in week:
                if day == 0:
                    temp_list.append([" ", "none"])
                elif str(day) == self.selected_date:
                    temp_list.append([str(day), "rgba(0, 255, 0, 0.05)"])
                else:
                    temp_list.append([str(day), "rgba(255, 255, 255, 0.05)"])

            self.calendar_data.append(temp_list)

    # define month classes as per Python calendar module
    month_class: dict[int, str] = {
        1: "1월",
        2: "2월",
        3: "3월",
        4: "4월",
        5: "5월",
        6: "6월",
        7: "7월",
        8: "8월",
        9: "9월",
        10: "10월",
        11: "11월",
        12: "12월",
    }

    # define days of the week
    date_class: dict[int, str] = {
        0: "월",
        1: "화",
        2: "수",
        3: "목",
        4: "금",
        5: "토",
        6: "일",
    }

    # define method to change month (and eyar)
    def delta_calendar(self, delta: int):
        if delta == 1:
            if self.month + delta > 12:
                self.month = 1
                self.year += 1
            else:
                self.month += 1

        if delta == -1:
            if self.month + delta < 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1

        self.clear_calendar_grid()
        self.get_calendar_data()