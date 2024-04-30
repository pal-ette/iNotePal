import datetime
import reflex as rx
import calendar

cal = calendar.Calendar()

# define a set of heat signature colors
colors = [
    # ... (color data) ...
]


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
