from reflex_calendar import calendar

import reflex as rx
import datetime

# related to calendar module


class aCalendar(rx.State):
    selected_date: str = ""
    logs: list[str] = []
    start_day: str = ""
    end_day: str = ""
    isStart: bool = True
    date_valid_check: bool = True
    graph_valid_check: bool = False

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
        if self.end_day != "":
            self.compare_dates()

    def setEndDay(self):
        self.end_day = self.selected_date
        if self.start_day != "":
            self.compare_dates()

    def reset_date_valid_check(self):
        self.date_valid_check = True

    def reset_graph_valid_check(self):
        self.graph_valid_check = False

    # def get_date_input(year, month, day):
    #     return datetime.date(year, month, day)

    def compare_dates(self):
        start_day_list = self.start_day.split()
        end_day_list = self.end_day.split()

        year_s, month_s, day_s = (
            int(start_day_list[3]),
            month_to_number(start_day_list[1]),
            int(start_day_list[2]),
        )
        year_e, month_e, day_e = (
            int(end_day_list[3]),
            month_to_number(end_day_list[1]),
            int(end_day_list[2]),
        )

        start_date_c = datetime.date(year_s, month_s, day_s)
        end_date_c = datetime.date(year_e, month_e, day_e)

        if end_date_c < start_date_c:
            self.date_valid_check = False
            self.graph_valid_check = False

            print("종료 날짜가 시작 날짜보다 앞섭니다. 다시 입력하세요.")
            self.start_day = ""
            self.end_day = ""
        else:
            self.graph_valid_check = True


def month_to_number(month_name):
    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    return months[month_name]


# 함수 호출
# compare_dates()


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


data2 = [
    {
        "emotion": "기쁨",
        "count": 120,
    },
    {
        "emotion": "놀람",
        "count": 98,
    },
    {
        "emotion": "분노",
        "count": 86,
    },
    {
        "emotion": "슬픔",
        "count": 99,
    },
    {
        "emotion": "중립",
        "count": 85,
    },
    {
        "emotion": "혐오",
        "count": 65,
    },
    {
        "emotion": "공포",
        "count": 65,
    },
]

# 공포 기쁨 놀람 분노 슬픔 중립 혐오
data_funnel = [
    {"value": 100, "enotion": "공포", "fill": "#8884d8"},
    {"value": 80, "name": "기쁨", "fill": "#83a6ed"},
    {"value": 50, "name": "놀람", "fill": "#8dd1e1"},
    {"value": 40, "name": "분노", "fill": "#82ca9d"},
    {"value": 26, "name": "슬픔", "fill": "#a4de6c"},
    {"value": 40, "name": "중립", "fill": "#82ca9d"},
    {"value": 26, "name": "혐오", "fill": "#a4de6c"},
]


class chart(rx.State):
    radar_chart_check: bool = False
    funnel_chart_check: bool = False
    bar_chart_check: bool = False
    line_chart_check: bool = False

    def radar_chart_status(self):
        self.radar_chart_check = not (self.radar_chart_check)

    def funnel_chart_status(self):
        self.funnel_chart_check = not (self.funnel_chart_check)

    def bar_chart_status(self):
        self.bar_chart_check = not (self.bar_chart_check)

    def line_chart_status(self):
        self.line_chart_check = not (self.line_chart_check)
