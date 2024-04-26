from reflex_calendar import calendar

import reflex as rx


# related to calendar module


class aCalendar(rx.State):
    selected_date: str = ""
    logs: list[str] = []
    start_day: str = ""
    end_day: str = ""
    isStart: bool = True

    def change_handler(self, var):
        self.selected_date = var
        self.add_log(f"Changed selected date: {var}")

    def active_start_date_change_handler(self, var):
        if "drill" in var["action"]:
            return

        action = var["action"]
        start_date = var["activeStartDate"]
        self.add_log(f"Changed active start date to {start_date} ({action})")

    def click_day_handler(self, day):
        self.add_log(f"Clicked day {day}")

    def click_month_handler(self, month):
        self.add_log(f"Clicked month {month}")

    def click_decade_handler(self, var):
        self.add_log(f"Clicked decade {var}")

    def click_year_handler(self, year):
        self.add_log(f"Clicked year {year}")

    def click_week_number_handler(self, var):
        self.add_log(f"Clicked week number {var['week_number']}")

    def drill_down_handler(self, view):
        self.add_log(f"Drilled down to: {view} view")

    def drill_up_handler(self, view):
        self.add_log(f"Drilled up to: {view} view")

    def view_change_handler(self, event):
        self.add_log(f"View changed to: {event['view']}")

    def clear_logs(self):
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)
        if len(self.logs) > 15:
            self.logs.pop(0)

    def setStartDay(self):
        self.start_day = self.selected_date
        print("start_day : ", self.start_day)

    def setEndDay(self):
        self.end_day = self.selected_date
        print("end_day : ", self.end_day)


def logs():
    return rx.vstack(
        rx.heading("Logs", size="6"),
        rx.foreach(
            aCalendar.logs,
            lambda log: rx.text(log, color="gray", size="3"),
        ),
        rx.spacer(),
        rx.button(
            "Clear Logs", on_click=aCalendar.clear_logs, size="3", color_scheme="ruby"
        ),
        align="center",
        width="50%",
        height="100%",
        spacing="1",
    )


def demo():
    return rx.vstack(
        rx.heading("Calendar Demo", size="6"),
        # rx.moment(Calendar.selected_date),
        calendar(
            go_to_range_start_on_select=True,
            locale="ko-KR",
            on_active_start_date_change=aCalendar.active_start_date_change_handler,
            on_change=aCalendar.change_handler,
            on_click_day=aCalendar.click_day_handler,
            on_click_month=aCalendar.click_month_handler,
            on_click_decade=aCalendar.click_decade_handler,
            on_click_year=aCalendar.click_year_handler,
            on_click_week_number=aCalendar.click_week_number_handler,
            on_drill_down=aCalendar.drill_down_handler,
            on_drill_up=aCalendar.drill_up_handler,
            on_view_change=aCalendar.view_change_handler,
        ),
        align="center",
        width="100%",
    )


# def setStartDay(self):
#     if isStart:
#         self.start_day = self.selected_data
#         print(f"start day: {self.start_day} ")
#     else:
#         self.end_day =  self.selected_data
#         print(f"start day: {self.start_day} ")


# def setEndDay(self):
#     self.end_day = self.selected_data
#     print("end day: ", self.end_day)


# @rx.var
# def isStart(self) -> bool:
#     return True
