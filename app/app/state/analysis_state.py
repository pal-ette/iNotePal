import reflex as rx
from datetime import date, timedelta
from app.state.chat_state import ChatState
from typing import List, Dict
from collections import defaultdict
from app.util.emotion import emotion_color_map as emotion_color_map_raw
from konlpy.tag import Kkma
from collections import Counter


class AnalysisState(ChatState):
    start_day: date = date.today() - timedelta(days=30)
    end_day: date = date.today()
    date_valid_check: bool = True

    def on_change_date(self, year, month, day):
        self.select_date = date(year, month, day)

    def onOpenChangeStartDay(self, isOpen):
        if isOpen:
            self.reset_calendar_date(self.start_day)
        else:
            self.setStartDay()

    def onOpenChangeEndDay(self, isOpen):
        if isOpen:
            self.reset_calendar_date(self.end_day)
        else:
            self.setEndDay()

    def setStartDay(self):
        if not self.is_valid_date_range(self.select_date, self.end_day):
            self.reset_calendar_date(self.start_day)
            self.date_valid_check = False
            return

        self.start_day = self.select_date

    def setEndDay(self):
        if not self.is_valid_date_range(self.start_day, self.select_date):
            self.reset_calendar_date(self.end_day)
            self.date_valid_check = False
            return

        self.end_day = self.select_date

    def reset_calendar_date(self, new_date):
        self.select_date = new_date

    def reset_calendar_today(self):
        self.reset_calendar_date(date.today())

    def reset_date_valid_check(self):
        self.date_valid_check = True

    @rx.var
    def start_year(self):
        return self.start_day.year

    @rx.var
    def start_month(self):
        return self.start_day.month

    @rx.var
    def end_year(self):
        return self.end_day.year

    @rx.var
    def end_month(self):
        return self.end_day.month

    @rx.var
    def emotion_color_map(self) -> Dict[str, str]:
        return emotion_color_map_raw

    @rx.var
    def print_start_day_text(self):
        text_date = (
            f"{self.start_day.year}년 {self.start_day.month}월 {self.start_day.day}일"
        )
        return text_date

    @rx.var
    def print_end_day_text(self):
        text_date = f"{self.end_day.year}년 {self.end_day.month}월 {self.end_day.day}일"
        return text_date

    def is_valid_date_range(self, start: date, end: date):
        return end >= start

    @rx.var(cache=True)
    def data_emotion(self):
        period_data = self.get_chats_in_period(
            self.start_day,
            self.end_day,
        )
        return [
            message.emotion.value
            for item in period_data
            for message in item.messages
            if message.is_user and message.emotion
        ]

    @rx.var(cache=True)
    def data_emotion_total(self):
        start_day = date(1970, 1, 1)
        end_day = date(2999, 12, 31)

        total_data = self.get_chats_in_period(
            start_day,
            end_day,
        )
        return [
            message.emotion.value
            for item in total_data
            for message in item.messages
            if message.is_user and message.emotion
        ]

    @rx.var(cache=True)
    def data_emotion_count(self):
        emotion_count = {emotion: 0 for emotion in emotion_color_map_raw}
        for emotion in self.data_emotion:
            emotion_count[emotion] += 1
        return emotion_count

    @rx.var(cache=True)
    def data_emotion_count_total(self):
        emotion_count_total = {emotion: 0 for emotion in emotion_color_map_raw}
        for emotion in self.data_emotion_total:
            emotion_count_total[emotion] += 1
        return emotion_count_total

    @rx.var
    def data_emotion_radar(self) -> List[Dict[str, str | int]]:
        period_emotion_count = self.data_emotion_count
        total_emotion_count = self.data_emotion_count_total
        return [
            {
                "emotion": emotion,
                "period": period_emotion_count[emotion],
                "total": total_emotion_count[emotion],
            }
            for emotion in emotion_color_map_raw
        ]

    @rx.var
    def data_emotion_funnel(self) -> List[Dict[str, str | int]]:
        data_funnel = [
            {
                "emotion": emotion,
                "count": count,
                "fill": emotion_color_map_raw[emotion],
            }
            for emotion, count in self.data_emotion_count.items()
            if count > 0 and emotion in emotion_color_map_raw
        ]
        return sorted(data_funnel, key=lambda x: x["count"], reverse=True)

    @rx.var
    def count_emotions_by_date(self):
        period_data = self.get_chats_in_period(
            self.start_day,
            self.end_day,
        )
        emotions_by_date = defaultdict(lambda: defaultdict(int))

        for entry in period_data:
            for message in entry.messages:
                if message.emotion and message.is_user:
                    emotion = message.emotion.value
                    if emotion:
                        emotions_by_date[entry.date][emotion] += 1

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
    def display_words(self) -> List[Dict[str, str | int]]:
        kkma = Kkma()
        including = ["NNG", "NNM", "NNP", "NP"]  # , "VA", "VV", "MA"]

        period_data = self.get_chats_in_period(
            self.start_day,
            self.end_day,
        )
        messages = [
            message.message
            for item in period_data
            for message in item.messages
            if message.is_user
        ]

        if messages == []:
            return messages

        messages = " ".join(messages)
        morphs = []
        pos = kkma.pos(messages)
        for w in pos:
            if w[1] in including:
                morphs.append(w[0])

        words_count = Counter(morphs)
        words = [
            {"text": key, "value": value}
            for i, (key, value) in enumerate(words_count.items())
        ]

        return words


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
