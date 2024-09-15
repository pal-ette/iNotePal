import reflex as rx
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


class Calendar(rx.ComponentState):
    year: int = datetime.datetime.now().year  # 연도 저장
    month: int = datetime.datetime.now().month  # 표시할 월 저장

    select_year: int = datetime.datetime.now().year
    select_month: int = datetime.datetime.now().month
    select_day: int = datetime.datetime.now().day

    @rx.var(cache=True)
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
                    f"{cls.month}월 {cls.year}",
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
                            data,
                            font_size="16px",
                            font_weight="bold",
                            align="center",
                        ),
                        style=cal_days_style,
                    )
                    for data in [
                        "월",
                        "화",
                        "수",
                        "목",
                        "금",
                        "토",
                        "일",
                    ]
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
                                        cls.set_selected_date(day),
                                        on_change(cls.year, cls.month, day),
                                    ],
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )


calendar_component = Calendar.create
