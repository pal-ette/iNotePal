import reflex as rx
from datetime import datetime, date, timedelta
from app.state.chat_state import ChatState
from typing import List, Dict
from collections import defaultdict
from app.util.emotion import emotion_color_map


class AnalysisState(ChatState):
    selected_date: date | None = None
    logs: list[str] = []
    start_day: date | None = date.today() - timedelta(days=30)
    end_day: date | None = date.today()
    isStart: bool = True
    date_valid_check: bool = True

    def on_change_day(self, day):
        self.select_year = self.year
        self.select_month = self.month
        self.day = day
        self.selected_date = date(self.year, self.month, self.day)

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

    def onOpenChangeStartDay(self, isOpen):
        if not isOpen:
            self.setStartDay()
            self.getDataDay()

    def onOpenChangeEndDay(self, isOpen):
        if not isOpen:
            self.setEndDay()
            self.getDataDay()

    def setStartDay(self):
        if self.selected_date == None:
            return

        if not self.is_valid_date_range(self.selected_date, self.end_day):
            self.date_valid_check = False
            return

        if self.start_day != None:
            self.data_reset()

        self.start_day = self.selected_date

    def setEndDay(self):
        if self.selected_date == None:
            return

        if not self.is_valid_date_range(self.start_day, self.selected_date):
            self.date_valid_check = False
            return

        if self.start_day != None:
            self.data_reset()

        self.start_day = self.selected_date

    def reset_date_valid_check(self):
        self.date_valid_check = True

    @rx.var
    def emotion_color_map(self) -> Dict[str, str]:
        return emotion_color_map

    @rx.var
    def print_start_day_text(self):
        if self.start_day == None:
            return " "

        text_date = (
            f"{self.start_day.year}년 {self.start_day.month}월 {self.start_day.day}일"
        )
        return text_date

    @rx.var
    def print_end_day_text(self):

        if self.end_day == None:
            return " "

        text_date = f"{self.end_day.year}년 {self.end_day.month}월 {self.end_day.day}일"
        return text_date

    def is_valid_date_range(self, start: date, end: date):
        return end >= start

    # chart
    radar_chart_check: bool = False
    funnel_chart_check: bool = False
    bar_chart_check: bool = False
    line_chart_check: bool = False

    def data_reset(self):
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

    @rx.var
    def data_emotion(self):
        if self.start_day == None:
            return []

        if self.end_day == None:
            return []

        period_data = self.get_chats_in_period(
            self.start_day.strftime("%Y-%m-%d"),
            self.end_day.strftime("%Y-%m-%d"),
        )
        return [
            message["emotion"]
            for item in period_data
            for message in item["message"]
            if message["is_user"] and message["emotion"]
        ]

    @rx.var
    def data_emotion_total(self):
        start_day = "1970-01-01"
        end_day = "2024-05-03"

        total_data = self.get_chats_in_period(start_day, end_day)
        return [
            message["emotion"]
            for item in total_data
            for message in item["message"]
            if message["is_user"] and message["emotion"]
        ]

    @rx.var
    def data_emotion_count(self):
        emotion_count = {
            "혐오": 0,
            "분노": 0,
            "공포": 0,
            "슬픔": 0,
            "중립": 0,
            "놀람": 0,
            "기쁨": 0,
        }
        for emotion in self.data_emotion:
            if emotion in emotion_count:
                emotion_count[emotion] += 1
            else:
                emotion_count[emotion] = 1
        return emotion_count

    @rx.var
    def data_emotion_count_total(self):
        emotion_count_total = {
            "혐오": 0,
            "분노": 0,
            "공포": 0,
            "슬픔": 0,
            "중립": 0,
            "놀람": 0,
            "기쁨": 0,
        }
        for emotion in self.data_emotion_total:
            if emotion in emotion_count_total:
                emotion_count_total[emotion] += 1
            else:
                emotion_count_total[emotion] = 1
        return emotion_count_total

    @rx.var
    def data_emotion_radar(self) -> List[Dict[str, str | int]]:
        data_radar = []
        period = [
            {"emotion": emotion, "count": count}
            for emotion, count in self.data_emotion_count.items()
        ]
        total = [
            {"emotion": emotion, "count": count}
            for emotion, count in self.data_emotion_count_total.items()
        ]
        data_radar = [
            {"emotion": p["emotion"], "period": p["count"], "total": t["count"]}
            for p, t in zip(period, total)
        ]
        return data_radar

    @rx.var
    def data_emotion_funnel(self) -> List[Dict[str, str | int]]:
        data_funnel = []
        for emotion, count in self.data_emotion_count.items():
            if count == 0:
                continue
            if emotion in emotion_color_map:
                new_dict = {
                    "emotion": emotion,
                    "count": count,
                    "fill": emotion_color_map[emotion],
                }
                data_funnel.append(new_dict)

        data_funnel = sorted(data_funnel, key=lambda x: x["count"], reverse=True)
        return data_funnel

    @rx.var
    def count_emotions_by_date(self):
        if self.start_day == None:
            return []
        if self.end_day == None:
            return []

        period_data = self.get_chats_in_period(
            self.start_day.strftime("%Y-%m-%d"),
            self.end_day.strftime("%Y-%m-%d"),
        )
        emotions_by_date = defaultdict(lambda: defaultdict(int))

        for entry in period_data:
            if "message" in entry:
                for message in entry["message"]:
                    if message["emotion"] and message["is_user"]:
                        emotion = message["emotion"]
                        if emotion:
                            emotions_by_date[entry["date"]][emotion] += 1

        emotions_list = []
        for date, emotions in emotions_by_date.items():
            emotions_list.append({"date": date, "emotions": dict(emotions)})

        return emotions_list

    @rx.var
    def data_emotion_bar(self) -> List[Dict[str, str | int]]:
        emotion_totals = defaultdict(
            lambda: {
                "공포": 0,
                "기쁨": 0,
                "놀람": 0,
                "분노": 0,
                "슬픔": 0,
                "중립": 0,
                "혐오": 0,
            }
        )

        data_bar = []
        for entry in self.count_emotions_by_date:

            date = entry["date"]
            emotions = entry["emotions"]
            for emotion, count in emotions.items():
                emotion_totals[date][emotion] += count

        transformed_data = [
            {"date": date, **emotions} for date, emotions in emotion_totals.items()
        ]
        data_bar = sorted(transformed_data, key=lambda x: x["date"], reverse=False)
        return data_bar

    @rx.var
    def data_emotion_line(self) -> List[Dict[str, str | int]]:

        data_line = []
        for emotion, count in self.data_emotion_count.items():
            if count == 0:
                continue

        return data_line

    def set_emotion_counts_state(self):
        self.emotion_counts_check = False

    def set_data_radar_state(self):
        self.data_radar_check = False

    def set_data_funnel_state(self):
        self.data_funnel_check = False

    def data_bar_state(self):
        self.data_bar_check = False

    def data_line_state(self):
        self.data_line_check = False

    def getDataDay(self):
        if self.start_day != "" and self.end_day != "":
            period_data = self.get_chats_in_period(
                self.start_day.strftime("%Y-%m-%d"),
                self.end_day.strftime("%Y-%m-%d"),
            )

            for item in period_data:
                for message in item["message"]:
                    if message["is_user"] and message["emotion"] is not None:
                        self.emotions_list.append(message["emotion"])
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

            self.set_emotion_counts_state()

    def getDataRadar(self):
        if self.emotion_counts_check:
            self.emotion_count_day()

        if self.data_radar_check:
            self.set_data_radar_state()

    def getDataFunnels(self):
        if self.emotion_counts_check:
            self.emotion_count_day()

        if self.data_funnel_check:

            for emotion, count in self.emotion_counts.items():
                if count == 0:
                    continue
                if emotion in emotion_color_map:
                    new_dict = {
                        "emotion": emotion,
                        "count": count,
                        "fill": emotion_color_map[emotion],
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
