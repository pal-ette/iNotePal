import reflex as rx
from app.app_state import AppState
import datetime
import calendar
from typing import List

cal = calendar.Calendar()


cal_days_style = {
    "width": "50px",
    "height": "50px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "border_radius": "6px",
}
# 캘린더 행 스타일 정의
cal_row_style = {
    "width": "50px",
    "height": "50px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "border_radius": "6px",
}

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

date_class: dict[int, str] = {
    0: "월",
    1: "화",
    2: "수",
    3: "목",
    4: "금",
    5: "토",
    6: "일",
}


class Calendar(rx.ComponentState):
    year: int = datetime.datetime.now().year  # 연도 저장
    month: int = datetime.datetime.now().month  # 표시할 월 저장

    select_year: int | None = None
    select_month: int | None = None
    select_day: int | None = None

    @rx.var
    def monthdayscalendar(self) -> List[List[int]]:
        return cal.monthdayscalendar(self.year, self.month)

    def set_selected_date(self, day):
        if day == 0:
            return
        if (
            (self.select_year == self.year)
            and (self.select_month == self.month)
            and (self.select_day == day)
        ):
            self.select_year = None
            self.select_month = None
            self.select_day = None
        else:
            self.select_year = self.year
            self.select_month = self.month
            self.select_day = day

    def delta_calendar(self, delta: int):
        if delta == 1:
            if (
                self.month + delta > 12
            ):  # # 12월을 넘어가면, 연도를 +1하고, 월을 1로 설정
                self.month = 1
                self.year += 1
            else:
                self.month += 1

        # 1월 이전이면, 연도를 -1하고, 월을 12로 설정
        if delta == -1:
            if self.month + delta < 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1

    @classmethod
    def get_component(cls, *children, **props) -> rx.Component:

        on_change = props.pop("on_change")

        return rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="chevron_left",
                    cursor="pointer",
                    on_click=cls.delta_calendar(-1),
                ),
                rx.spacer(),  # 빈 공간 생성
                rx.text(  # 현재 월과 연도를 표시하는 텍스트
                    f"{cls.month} {cls.year}",
                    width="150px",
                    display="flex",
                    justify_content="center",
                ),
                rx.spacer(),
                rx.icon(
                    tag="chevron_right",
                    cursor="pointer",
                    on_click=cls.delta_calendar(1),
                ),
                display="flex",
                align_items="center",
                justify_content="center",
                spacing="2",
            ),
            rx.hstack(
                *[
                    rx.container(
                        rx.text(
                            date_class[data],
                            font_size="16px",
                            font_weight="bold",
                            align="center",
                        ),
                        style=cal_days_style,
                    )
                    for data in date_class
                ]
            ),
            rx.vstack(
                rx.foreach(
                    cls.monthdayscalendar,
                    lambda week: rx.hstack(
                        rx.foreach(
                            week,
                            lambda day: rx.cond(
                                day == 0,
                                rx.container(
                                    rx.text(
                                        " ",
                                        font_size="14px",
                                        align="center",
                                    ),
                                    style=cal_row_style,
                                ),
                                rx.container(
                                    rx.text(
                                        day,
                                        font_size="14px",
                                        align="center",
                                    ),
                                    background_color=rx.cond(
                                        (cls.year == cls.select_year)
                                        & (cls.month == cls.select_month)
                                        & (day == cls.select_day),
                                        "#e5988e",
                                        "rgba(255, 255, 255, 0.05)",
                                    ),
                                    style=cal_row_style,
                                    cursor="pointer",  # Make clickable
                                    on_click=[
                                        on_change(cls.year, cls.month, day),
                                        cls.set_selected_date(day),
                                    ],
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )


calendar_component = Calendar.create


# class_State 분리
# 캘린더 UI, 연도, 월, 선택된 날짜, 캘린더 그리드 데이터 관리하는 클래스
class State(rx.State):
    year: int = datetime.datetime.now().year  # 연도 저장
    month: int = datetime.datetime.now().month  # 표시할 월 저장

    # calendar_data: list[list[str]]  # 데이터 저장 변수

    # 현재 선택된 날짜를 저장하는 변수 지정, 선택전에는 None 상태
    selected_date: str | None = None  # Add to track selected date
    # 날짜 변경시 호출되는 콜백함수 저장
    _on_change = None

    # 날짜 선택되었을 때 호출되는 메서드
    def select_date(self, date: str) -> None:
        self.selected_date = date
        # if self._on_change:
        #     self._on_change(date)
        # self.get_calendar_data()        # 함수 호출해 선택된 날짜 반영하여 캘린더 그리드 재 생성

    # 캘린더 그리드의 데이터 초기화
    def clear_calendar_grid(self):
        self.calendar_data = []

    # 그리드를 채우는 방법 정의
    # python의 calendar 모듈 활용하여 선택된 연도와 월에 대한 캘린더 데이터 생성
    @rx.var
    def calendar_data(self) -> list[list[str]]:
        calendar_data = []
        for week in cal.monthdayscalendar(
            self.year, self.month
        ):  # 월별 일정 데이터 가져온다
            temp_list: list = []
            for day in week:
                if day == 0:
                    temp_list.append([" ", "none"])
                elif str(day) == self.selected_date:
                    temp_list.append([str(day), "rgba(0, 255, 0, 0.05)"])
                else:
                    temp_list.append([str(day), "rgba(255, 255, 255, 0.05)"])

            calendar_data.append(temp_list)
        return calendar_data

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

    # define method to change month (and year)
    # 이전달 또는 다음달로 이동하는 기능을 수행
    def delta_calendar(self, delta: int):
        if delta == 1:
            if (
                self.month + delta > 12
            ):  # # 12월을 넘어가면, 연도를 +1하고, 월을 1로 설정
                self.month = 1
                self.year += 1
            else:
                self.month += 1

        # 1월 이전이면, 연도를 -1하고, 월을 12로 설정
        if delta == -1:
            if self.month + delta < 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1

        self.clear_calendar_grid()
        # self.get_calendar_data()
