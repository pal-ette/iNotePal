from reflex_calendar import calendar

import reflex as rx
from datetime import datetime
from app.state.chat_state import ChatState
from typing import List, Dict
from reflex_calendar import reformat_date
import json


class AnalysisState(ChatState):
    selected_date: str = ""
    logs: list[str] = []
    start_day: str = ""
    end_day: str = ""
    isStart: bool = True
    date_valid_check: bool = True
    graph_valid_check: bool = False

    start_date_c: str = ""
    end_date_c: str = ""

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
        print("end data pre set: ", self.end_day)

        if self.start_day != "":
            self.data_reset()

        self.start_day = self.selected_date
        if self.end_day and all(
            [c.isalpha() or c.isdigit() or c.isspace() for c in self.end_day]
        ):
            self.compare_dates()

    def setEndDay(self):

        if self.end_day != "":
            self.data_reset()

        self.end_day = self.selected_date
        if self.start_day and all(
            [c.isalpha() or c.isdigit() or c.isspace() for c in self.start_day]
        ):
            self.compare_dates()

    def reset_date_valid_check(self):
        self.date_valid_check = True

    def reset_graph_valid_check(self):
        self.graph_valid_check = False

    def compare_dates(self):

        self.start_date_c = datetime.strptime(self.start_day, "%a %b %d %Y")
        self.end_date_c = datetime.strptime(self.end_day, "%a %b %d %Y")

        if self.end_date_c < self.start_date_c:
            self.date_valid_check = False
            self.graph_valid_check = False

            print("종료 날짜가 시작 날짜보다 앞섭니다. 다시 입력하세요.")
            self.start_day = ""
            self.end_day = ""
        else:
            self.graph_valid_check = True

    # chart
    radar_chart_check: bool = False
    funnel_chart_check: bool = False
    bar_chart_check: bool = False
    line_chart_check: bool = False

    def data_reset(self):
        print("RESET DATA")
        self.radar_chart_check = False
        self.funnel_chart_check = False
        self.bar_chart_check = False
        self.line_chart_check = False

        self.emotion_counts_check = True

        self.data_radar_check = True
        self.data_funnel_check = True
        self.data_bar_check = True
        self.data_line_check = True

        self.emotions_list = []
        self.emotion_counts = {
            "혐오": 0,
            "분노": 0,
            "공포": 0,
            "슬픔": 0,
            "중립": 0,
            "놀람": 0,
            "기쁨": 0,
        }
        self.data_emotion_frequency = []
        self.data_funnel = []

    def radar_chart_status(self):
        self.radar_chart_check = not (self.radar_chart_check)

    def funnel_chart_status(self):
        self.funnel_chart_check = not (self.funnel_chart_check)

    def bar_chart_status(self):
        self.bar_chart_check = not (self.bar_chart_check)

    def line_chart_status(self):
        self.line_chart_check = not (self.line_chart_check)

    # getData

    data_radar_check: bool = True
    data_funnel_check: bool = True
    data_bar_check: bool = True
    data_line_check: bool = True
    emotion_counts_check: bool = True

    emotions_list: list[str] = []
    emotion_counts = {
        "혐오": 0,
        "분노": 0,
        "공포": 0,
        "슬픔": 0,
        "중립": 0,
        "놀람": 0,
        "기쁨": 0,
    }
    data_emotion_frequency: List[Dict[str, int]] = []
    data_funnel: List[Dict[int, str]] = []

    def set_emotion_counts_state(self):
        self.emotion_counts_check = False
        print("emotion_counts_state->False")

    def set_data_radar_state(self):
        self.data_radar_check = False
        print("data_radar_check --> False")

    def set_data_funnel_state(self):
        self.data_funnel_check = False
        print("data_funnel_check --> False")

    def data_bar_state(self):
        self.data_bar_check = False

    def data_line_state(self):
        self.data_line_check = False

    def getDataDay(self):
        # past_chats = self.past_messages

        if self.start_day != "":
            formatted_date_s = format_date(str(self.start_day))
            print("start day ", formatted_date_s)

        if self.end_day != "":
            formatted_date_e = format_date(str(self.end_day))
            print("end day ", formatted_date_e)

        if self.start_day != "" and self.end_day != "":
            period_data = self.get_chats_in_period(formatted_date_s, formatted_date_e)
            # print("period data: ", period_data)

            for item in period_data:
                for message in item["message"]:
                    if message["is_user"] and message["emotion"] is not None:
                        self.emotions_list.append(message["emotion"])

            print(self.emotions_list)

        yield

    def emotion_count_day(self):

        if self.emotion_counts_check:
            for emotion in self.emotions_list:
                if emotion in self.emotion_counts:
                    self.emotion_counts[emotion] += 1
                else:
                    self.emotion_counts[emotion] = 1
            self.data_emotion_frequency = [
                {"emotion": emotion, "count": count}
                for emotion, count in self.emotion_counts.items()
            ]

            print(self.data_emotion_frequency)
            self.set_emotion_counts_state()

    def getDataRadar(self):
        if self.emotion_counts_check:
            self.emotion_count_day()
            print("emotion_counts_check --> True")

        if self.data_radar_check:
            self.set_data_radar_state()
            print("data_radar_check --> True")

    def getDataFunnels(self):

        fill_mapping = {
            "혐오": "#49312d",
            "분노": "#91615a",
            "공포": "#af625c",
            "슬픔": "#de776c",
            "중립": "#e5988e",
            "놀람": "#ebb9b0",
            "기쁨": "#f2ebc8",
        }
        if self.emotion_counts_check:
            self.emotion_count_day()
            print("emotion_counts_check --> True")

        if self.data_funnel_check:
            print("data_funnel_check --> True")
            for emotion, count in self.emotion_counts.items():
                if count == 0:
                    continue
                if emotion in fill_mapping:
                    new_dict = {
                        "emotion": emotion,
                        "count": count,
                        "fill": fill_mapping[emotion],
                    }
                    self.data_funnel.append(new_dict)

            self.data_funnel = sorted(
                self.data_funnel, key=lambda x: x["count"], reverse=True
            )
            self.set_data_funnel_state()


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


def logs():
    return rx.vstack(
        rx.heading("Logs", size="6"),
        rx.foreach(
            AnalysisState.logs,
            lambda log: rx.text(log, color="gray", size="3"),
        ),
        rx.spacer(),
        rx.button(
            "Clear Logs",
            on_click=AnalysisState.clear_logs,
            size="3",
            color_scheme="ruby",
        ),
        align="center",
        width="50%",
        height="100%",
        spacing="1",
    )


def demo():
    return rx.vstack(
        # rx.heading("Calendar Demo", size="6"),
        # rx.moment(Calendar.selected_date),
        calendar(
            go_to_range_start_on_select=True,
            locale="ko-KR",
            on_active_start_date_change=AnalysisState.active_start_date_change_handler,
            on_change=AnalysisState.change_handler,
            on_click_day=AnalysisState.click_day_handler,
            on_click_month=AnalysisState.click_month_handler,
            on_click_decade=AnalysisState.click_decade_handler,
            on_click_year=AnalysisState.click_year_handler,
            on_click_week_number=AnalysisState.click_week_number_handler,
            on_drill_down=AnalysisState.drill_down_handler,
            on_drill_up=AnalysisState.drill_up_handler,
            on_view_change=AnalysisState.view_change_handler,
        ),
        align="center",
        width="100%",
    )


def format_date(date_str):

    date_object = datetime.strptime(date_str, "%a %b %d %Y")
    return date_object.strftime("%Y-%m-%d")


# # 데이터 정의
# data = [
#     {'date': '2024-05-02',
#       'user_id': '10a8355a-ce4f-42a7-9752-e4ac94d3059e',
#       'id': 318,
#       'is_closed': True,
#       'created_at': '2024-05-02T00:23:46.977442+00:00',
#       'emotion': '놀람',
#        'message': [{ 'id': 936,
#                     'chat_id': 318,
#                     'emotion': '공포',
#                     'is_user': True,
#                       'message': '몽아',
#                       'created_at': '2024-05-02T01:09:24.025188+00:00'},
#                         {'id': 937, 'chat_id': 318,
#                          'emotion': None,
#                          'is_user': False,
#                          'message': '기다리던 아이가 생기다니 기쁘시겠어요. 건강하게 출산이 어려울까 걱정되시는군요.',
#                 'created_at': '2024-05-02T01:09:28.582299+00:00'},
# {'id': 938, 'chat_id': 318, 'emotion': '혐오', 'is_user': True, 'message': '나나', 'created_at': '2024-05-02T01:09:30.999665+00:00'}, {'id': 939, 'chat_id': 318, 'emotion': None, 'is_user': False, 'message': '그런 말을 들으시다니 당황스러우셨겠어요. 건강이 걱정되고 혼란스러우시겠어요. 이런 상황에서 어떻게 하는 것이 좋은 방법일까요?', 'created_at': '2024-05-02T01:09:32.868334+00:00'}, {'id': 940, 'chat_id': 318, 'emotion': '슬픔', 'is_user': True, 'message': '카카', 'created_at': '2024-05-02T01:09:34.458762+00:00'}, {'id': 941, 'chat_id': 318, 'emotion': None, 'is_user': False, 'message': '그랬군요. 사장님한테 말씀 드렸어요? 그랬겠네요. 그래도 고의로 그런 거 아니니 이해하실 거예요.', 'created_at': '2024-05-02T01:09:35.66976+00:00'}, {'id': 942, 'chat_id': 318, 'emotion': '중립', 'is_user': True, 'message': '카카카', 'created_at': '2024-05-02T01:09:36.661925+00:00'}, {'id': 943, 'chat_id': 318, 'emotion': None, 'is_user': False, 'message': '혹시 업무에 어려움은 없으신가요? 나갈 때 차주들이 얘기를 안 하고 가나요?', 'created_at': '2024-05-02T01:09:37.214318+00:00'}, {'id': 944, 'chat_id': 318, 'emotion': '슬픔', 'is_user': True, 'message': 'ㅋㅋ', 'created_at': '2024-05-02T01:09:39.263435+00:00'}, {'id': 945, 'chat_id': 318, 'emotion': None, 'is_user': False, 'message': '무슨 일 있으세요? 무엇 때문에 그렇게 화가 나셨어요? 정말 속상하시겠어요! ',
