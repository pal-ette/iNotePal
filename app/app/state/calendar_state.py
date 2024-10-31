import reflex as rx
import datetime
import calendar
from typing import List

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
    day: int = datetime.datetime.now().day

    select_year: int = datetime.datetime.now().year
    select_month: int = datetime.datetime.now().month

    @rx.var()
    def monthdayscalendar(self) -> List[List[int]]:
        return calendar.Calendar().monthdayscalendar(self.year, self.month)

    def next_month(self):
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1

    def prev_month(self):
        if self.month == 1:
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1

    def set_month(self, month: int):
        self.month = month

    def set_day(self, day: int):
        self.select_year = self.year
        self.select_month = self.month
        self.day = day

    @classmethod
    def get_component(cls, *children, **props) -> rx.Component:
        prop_year = props.pop("year", cls.year)
        prop_select_year = props.pop("select_year", cls.select_year)
        prop_month = props.pop("month", cls.month)
        prop_select_month = props.pop("select_month", cls.select_month)
        prop_day = props.pop("day", cls.day)
        prop_monthdayscalendar = props.pop("monthdayscalendar", cls.monthdayscalendar)

        on_next_month = props.pop("on_next_month", cls.next_month)
        on_prev_month = props.pop("on_prev_month", cls.prev_month)
        on_change_month = props.pop("on_change_month", cls.set_month)
        on_change_day = props.pop("on_change_day", cls.set_day)

        return rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        tag="chevron_left",
                        cursor="pointer",
                        on_click=on_prev_month,
                    ),
                    rx.spacer(),  # 빈 공간 생성
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                rx.text(  # 현재 월과 연도를 표시하는 텍스트
                                    f"{prop_month}월 {prop_year}",
                                    width="150px",
                                    display="flex",
                                    justify_content="center",
                                    high_contrast=True,
                                ),
                                variant="ghost",
                            ),
                        ),
                        rx.popover.content(
                            rx.vstack(
                                rx.foreach(
                                    [
                                        [1, 2, 3, 4],
                                        [5, 6, 7, 8],
                                        [9, 10, 11, 12],
                                    ],
                                    lambda month_row: rx.hstack(
                                        rx.foreach(
                                            month_row,
                                            lambda month: rx.container(
                                                rx.text(
                                                    month,
                                                    font_size="14px",
                                                    align="center",
                                                ),
                                                background_color=rx.cond(
                                                    prop_month == month,
                                                    "#e5988e",
                                                    "rgba(255, 255, 255, 0.05)",
                                                ),
                                                style=cal_row_style,
                                                cursor="pointer",
                                                on_click=on_change_month(
                                                    month,
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        modal=True,
                    ),
                    rx.spacer(),
                    rx.icon(
                        tag="chevron_right",
                        cursor="pointer",
                        on_click=on_next_month,
                    ),
                    align="center",
                    justify="center",
                    spacing="2",
                ),
                children,
                width="100%",
                align="center",
                justify="between",
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
                    prop_monthdayscalendar,
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
                                        (prop_year == prop_select_year)
                                        & (prop_month == prop_select_month)
                                        & (day == prop_day),
                                        "#e5988e",
                                        "rgba(255, 255, 255, 0.05)",
                                    ),
                                    style=cal_row_style,
                                    cursor="pointer",  # Make clickable
                                    on_click=on_change_day(day),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )


calendar_component = Calendar.create
