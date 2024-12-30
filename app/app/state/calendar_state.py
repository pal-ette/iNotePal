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
    "position": "relative",
}


class Calendar(rx.ComponentState):
    year: int = date.today().year  # 연도 저장
    month: int = date.today().month  # 표시할 월 저장

    select_date: date = date.today()
    accent_dates: List[date] = [date(2024, 11, i) for i in range(1, 20)]

    allow_future: bool = True

    start_weekday = calendar.SUNDAY

    @rx.var(cache=True)
    def weekdays(self) -> List[str]:
        return [
            "월화수목금토일"[weekday % 7]
            for weekday in range(self.start_weekday, self.start_weekday + 7)
        ]

    @rx.var(cache=True)
    def monthdayscalendar(self) -> List[List[int]]:
        return calendar.Calendar(self.start_weekday).monthdayscalendar(
            self.year,
            self.month,
        )

    def next_month(self):
        if self.month == 12:
            if self.try_set_year(self.year + 1):
                self.month = 1
        else:
            self.month += 1

    def prev_month(self):
        if self.month == 1:
            if self.try_set_year(self.year - 1):
                self.month = 12
        else:
            self.month -= 1

    def is_valid_year_range(self, year):
        return MINYEAR <= year and year <= MAXYEAR

    def next_year(self):
        self.try_set_year(self.year + 1)

    def prev_year(self):
        self.try_set_year(self.year - 1)

    def on_change_year(self, year: str):
        try:
            parsed_year = int(year)
            self.try_set_year(parsed_year)
        except (ValueError, TypeError):
            pass

    def try_set_year(self, year: int) -> bool:
        if not self.is_valid_year_range(year):
            return False

        self.year = year
        return True

    def set_month(self, month: int):
        self.month = month

    def set_display_month(self, year: int, month: int):
        self.year = year
        self.month = month

    def on_change_date(self, year: int, month: int, day: int):
        self.select_date = date(year, month, day)

    def reset_to_today(self):
        self.year = date.today().year
        self.month = date.today().month

    def on_select_disabled_future(self, year: int, month: int, day: int):
        pass

    @classmethod
    def get_component(cls, *children, **props) -> rx.Component:
        prop_allow_future = props.pop("allow_future", cls.allow_future)
        prop_select_date = props.pop("select_date", cls.select_date)
        prop_accent_dates = props.pop("accent_dates", cls.accent_dates)
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
                                        on_change=cls.on_change_year,
                                    ),
                                    rx.icon(
                                        tag="chevron_right",
                                        cursor="pointer",
                                        on_click=cls.next_year,
                                    ),
                                    align="center",
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
                rx.hstack(
                    rx.button(
                        "오늘",
                        size="1",
                        on_click=[
                            cls.reset_to_today,
                            on_change_date(
                                date.today().year,
                                date.today().month,
                                date.today().day,
                            ),
                        ],
                    ),
                    children,
                ),
                width="100%",
                align="center",
                justify="between",
            ),
            rx.hstack(
                rx.foreach(
                    cls.weekdays,
                    lambda weekday: rx.container(
                        rx.text(
                            weekday,
                            font_size="16px",
                            font_weight="bold",
                            align="center",
                        ),
                        style=cal_days_style,
                    ),
                ),
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
                                    rx.cond(
                                        prop_accent_dates.contains(
                                            f"{cls.year}-{rx.cond(cls.month < 10, '0', '')}{cls.month}-{rx.cond(day < 10, '0', '')}{day}"
                                        ),
                                        rx.text(
                                            "•",
                                            font_size="14px",
                                            align="center",
                                            style={
                                                "position": "absolute",
                                                "top": "29px",
                                                "left": "23px",
                                            },
                                        ),
                                    ),
                                    background_color=rx.cond(
                                        f"{cls.year}-{rx.cond(cls.month < 10, '0', '')}{cls.month}-{rx.cond(day < 10, '0', '')}{day}"
                                        == prop_select_date,
                                        "#e5988e",
                                        "rgba(255, 255, 255, 0.05)",
                                    ),
                                    style=cal_row_style,
                                    cursor="pointer",  # Make clickable
                                    on_click=rx.cond(
                                        prop_allow_future
                                        | (
                                            (cls.year <= date.today().year)
                                            & (cls.month <= date.today().month)
                                            & (day <= date.today().day)
                                        ),
                                        on_change_date(cls.year, cls.month, day),
                                        cls.on_select_disabled_future(
                                            cls.year,
                                            cls.month,
                                            day,
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )


calendar_component = Calendar.create
