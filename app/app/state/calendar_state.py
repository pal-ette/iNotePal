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
        new_month = self.month + 1
        if new_month < 13:
            self.month = new_month
        elif self.try_set_year(self.year + 1):
            self.month = 1

    def prev_month(self):
        new_month = self.month - 1
        if new_month > 0:
            self.month = new_month
        elif self.try_set_year(self.year - 1):
            self.month = 12

    @rx.var(cache=True)
    def is_valid_next_month(self) -> bool:
        next_month = self.month + 1
        if next_month > 12:
            return self.is_valid_next_year
        elif not self.allow_future and self.year == date.today().year:
            return next_month <= date.today().month
        else:
            return True

    @rx.var(cache=True)
    def is_valid_prev_month(self) -> bool:
        prev_month = self.month - 1
        return self.is_valid_prev_year if prev_month < 1 else True

    def is_valid_year_range(self, year):
        return MINYEAR <= year and year <= (
            MAXYEAR if self.allow_future else date.today().year
        )

    def next_year(self):
        self.try_set_year(self.year + 1)

    def prev_year(self):
        self.try_set_year(self.year - 1)

    @rx.var(cache=True)
    def is_valid_prev_year(self) -> bool:
        return self.is_valid_year_range(self.year - 1)

    @rx.var(cache=True)
    def is_valid_next_year(self) -> bool:
        return self.is_valid_year_range(self.year + 1)

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
        if not self.allow_future and self.year == date.today().year:
            self.month = min(self.month, date.today().month)

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
        prop_select_date = props.pop("select_date", cls.select_date)
        prop_accent_dates = props.pop("accent_dates", cls.accent_dates)
        on_change_date = props.pop("on_change_date", cls.on_change_date)

        # Initialize using props with default fallback
        prop_allow_future = props.pop("allow_future", None)
        if prop_allow_future is not None:
            cls.__fields__["allow_future"].default = prop_allow_future

        return rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.button(
                        rx.icon(
                            tag="chevron_left",
                        ),
                        variant="ghost",
                        on_click=cls.prev_month,
                        disabled=~cls.is_valid_prev_month,
                    ),
                    rx.spacer(),  # 빈 공간 생성
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                rx.text(  # 현재 월과 연도를 표시하는 텍스트
                                    f"{cls.year}년 {cls.month}월",
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
                                    rx.button(
                                        rx.icon(
                                            tag="chevron_left",
                                        ),
                                        variant="ghost",
                                        on_click=cls.prev_year,
                                        disabled=~cls.is_valid_prev_year,
                                    ),
                                    rx.input(
                                        value=cls.year,
                                        max_length=4,
                                        on_change=cls.on_change_year,
                                    ),
                                    rx.button(
                                        rx.icon(
                                            tag="chevron_right",
                                        ),
                                        variant="ghost",
                                        on_click=cls.next_year,
                                        disabled=~cls.is_valid_next_year,
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
                                            lambda month: rx.button(
                                                rx.text(
                                                    month,
                                                    font_size="14px",
                                                    align="center",
                                                ),
                                                background_color=rx.cond(
                                                    cls.month == month,
                                                    "#e5988e",
                                                    "rgba(255, 255, 255, 0.0)",
                                                ),
                                                style=cal_row_style,
                                                on_click=cls.set_month(
                                                    month,
                                                ),
                                                variant="ghost",
                                                color=rx.cond(
                                                    cls.allow_future
                                                    | (cls.year < date.today().year)
                                                    | (
                                                        (cls.year == date.today().year)
                                                        & (month <= date.today().month)
                                                    ),
                                                    "currentColor",
                                                    rx.color_mode_cond(
                                                        light="#BBBBBB",
                                                        dark="#666666",
                                                    ),
                                                ),
                                                disabled=rx.cond(
                                                    cls.allow_future
                                                    | (cls.year < date.today().year)
                                                    | (
                                                        (cls.year == date.today().year)
                                                        & (month <= date.today().month)
                                                    ),
                                                    False,
                                                    True,
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
                    rx.button(
                        rx.icon(
                            tag="chevron_right",
                        ),
                        variant="ghost",
                        on_click=cls.next_month,
                        disabled=~cls.is_valid_next_month,
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
                            lambda day: rx.container(
                                rx.text(
                                    rx.cond(day == 0, " ", day),
                                    font_size="14px",
                                    color=rx.cond(
                                        (day > 0)
                                        & (
                                            cls.allow_future
                                            | (
                                                (
                                                    cls.year * 10000
                                                    + cls.month * 100
                                                    + day
                                                )
                                                <= (
                                                    date.today().year * 10000
                                                    + date.today().month * 100
                                                    + date.today().day
                                                )
                                            )
                                        ),
                                        "currentColor",
                                        rx.color_mode_cond(
                                            light="#BBBBBB",
                                            dark="#666666",
                                        ),
                                    ),
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
                                    "rgba(255, 255, 255, 0.0)",
                                ),
                                style=cal_row_style,
                                cursor=rx.cond(
                                    (day > 0)
                                    & (
                                        cls.allow_future
                                        | (
                                            (cls.year * 10000 + cls.month * 100 + day)
                                            <= (
                                                date.today().year * 10000
                                                + date.today().month * 100
                                                + date.today().day
                                            )
                                        )
                                    ),
                                    "pointer",
                                    "default",
                                ),
                                on_click=rx.cond(
                                    (day > 0)
                                    & (
                                        cls.allow_future
                                        | (
                                            (cls.year * 10000 + cls.month * 100 + day)
                                            <= (
                                                date.today().year * 10000
                                                + date.today().month * 100
                                                + date.today().day
                                            )
                                        )
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
        )


calendar_component = Calendar.create
