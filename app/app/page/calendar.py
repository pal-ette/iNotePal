import datetime
import reflex as rx
import calendar
from app.state.calendar_state import State

cal = calendar.Calendar()

# define styles
cal_days_style = {
    "width": "50px",
    "height": "50px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "border_radius": "6px",
}
cal_row_style = {
    "width": "50px",
    "height": "50px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "border_radius": "6px",
}


# define method to return text for days
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


#  define method to return grid row
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


# Reflex page definition
@rx.page(route="/calendar", on_load=State.get_calendar_data)
def index() -> rx.Component:
    return rx.vstack(
        # calendar start ...
        rx.hstack(
            rx.icon(
                tag="chevron_left", cursor="pointer", on_click=State.delta_calendar(-1)
            ),
            rx.spacer(),
            rx.text(
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
