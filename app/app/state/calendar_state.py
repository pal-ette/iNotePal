import reflex as rx
from datetime import date, MINYEAR, MAXYEAR
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
    year: int = date.today().year  # 연도 저장
    month: int = date.today().month  # 표시할 월 저장

    select_date: date = date.today()

    @rx.var()
    def monthdayscalendar(self) -> List[List[int]]:
        return calendar.Calendar().monthdayscalendar(self.year, self.month)

    def next_month(self):
        if self.month == 12 and self.is_valid_year_range(self.year + 1):
            self.year += 1
            self.month = 1
        else:
            self.month += 1

    def prev_month(self):
        if self.month == 1 and self.is_valid_year_range(self.year - 1):
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1

    def is_valid_year_range(self, year):
        return MINYEAR <= year and year <= MAXYEAR

    def next_year(self):
        if not self.is_valid_year_range(self.year + 1):
            return

        self.year += 1

    def prev_year(self):
        if not self.is_valid_year_range(self.year - 1):
            return

        self.year -= 1

    def set_year(self, year: str):
        try:
            self.year = int(year)
        except (ValueError, TypeError):
            pass

    def set_month(self, month: int):
        self.month = month

    def on_change_date(self, year: int, month: int, day: int):
        self.select_date = date(year, month, day)

    @classmethod
    def get_component(cls, *children, **props) -> rx.Component:
        prop_select_date = props.pop("select_date", cls.select_date)
        on_change_date = props.pop("on_change_date", cls.on_change_date)

        return rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        tag="chevron_left",
                        cursor="pointer",
                        on_click=cls.prev_month,
                    ),
                    rx.spacer(),  # 빈 공간 생성
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                rx.text(  # 현재 월과 연도를 표시하는 텍스트
                                    f"{cls.month}월 {cls.year}",
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
                                rx.hstack(
                                    rx.icon(
                                        tag="chevron_left",
                                        cursor="pointer",
                                        on_click=cls.prev_year,
                                    ),
                                    rx.input(
                                        value=cls.year,
                                        max_length=4,
                                        on_change=cls.set_year,
                                    ),
                                    rx.icon(
                                        tag="chevron_right",
                                        cursor="pointer",
                                        on_click=cls.next_year,
                                    ),
                                ),
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
                                                    cls.month == month,
                                                    "#e5988e",
                                                    "rgba(255, 255, 255, 0.05)",
                                                ),
                                                style=cal_row_style,
                                                cursor="pointer",
                                                on_click=cls.set_month(
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
                        on_click=cls.next_month,
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
                                        f"{cls.year}-{rx.cond(cls.month < 10, '0', '')}{cls.month}-{rx.cond(day < 10, '0', '')}{day}"
                                        == prop_select_date,
                                        "#e5988e",
                                        "rgba(255, 255, 255, 0.05)",
                                    ),
                                    style=cal_row_style,
                                    cursor="pointer",  # Make clickable
                                    on_click=on_change_date(cls.year, cls.month, day),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )


calendar_component = Calendar.create
