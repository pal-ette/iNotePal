import datetime
import reflex as rx
import calendar
from app.state.calendar_state import State

cal = calendar.Calendar()

# 캘린더 셀 스타일 정의
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


# 각 캘린더 셀 생성 함수, 날짜, 요일, 스타일 정보를 매겨변수로 받아 셀 요소로 반환
def calendar_days(data):
    return rx.container(
        rx.text(
            data[1],
            font_size="16px",
            font_weight="bold",
            align="center",
        ),
        style=cal_days_style,
    )


#  요일과 날짜를 포함하는 캘린더 행을 생성 함수
def calendar_grid_row(data: list[str]):
    date_str = data[0]
    return rx.container(
        rx.text(
            data[0],
            font_size="14px",
            align="center",
        ),
        background_color=data[1],
        style=cal_row_style,
        cursor="pointer",  # Make clickable
        on_click=lambda: State.select_date(date_str),  # Update on click
    )


# define method to return grid UI
def calendar_grid(data):
    return rx.vstack(
        rx.hstack(rx.foreach(data, calendar_grid_row)),
    )


# Reflex 화면 정의
@rx.page(route="/calendar")
def index() -> rx.Component:
    # vstack : 자식 요소(달/연 이동 버튼, 요일 표시, 캘린더 그리드)들을 세로로 쌓아 배치
    return rx.vstack(
        # calendar start ...
        # hsatack : 자식 요소들을 가로로 배치
        rx.hstack(
            rx.icon(
                tag="chevron_left", cursor="pointer", on_click=State.delta_calendar(-1)
            ),
            rx.spacer(),  # 빈 공간 생성
            rx.text(  # 현재 월과 연도를 표시하는 텍스트
                f"{State.month_class[State.month]} {State.year}",
                width="150px",
                display="flex",
                justify_content="center",
            ),
            rx.spacer(),
            rx.icon(
                tag="chevron_right", cursor="pointer", on_click=State.delta_calendar(1)
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            spacing="2",
        ),
        rx.hstack(
            # calendar days of the week
            rx.foreach(
                State.date_class,
                calendar_days,
            ),
        ),
        # calendar grid ...
        rx.foreach(
            State.calendar_data,
            calendar_grid,
        ),
    )
