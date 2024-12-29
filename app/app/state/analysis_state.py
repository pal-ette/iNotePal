import reflex as rx
from datetime import date, timedelta
from app.state.chat_state import ChatState
from typing import List, Dict
from collections import defaultdict
from konlpy.tag import Kkma
from collections import Counter


class AnalysisState(ChatState):
    start_date: date = date.today() - timedelta(days=30)
    end_date: date = date.today()
    range_select_date: date = date.today()
    date_valid_check: bool = True

    def on_change_date(self, year, month, day):
        self.range_select_date = date(year, month, day)

    def on_open_change_start_date(self, isOpen):
        if isOpen:
            self.reset_calendar_date(self.start_date)
        else:
            self.set_start_date()

    def on_open_change_end_date(self, isOpen):
        if isOpen:
            self.reset_calendar_date(self.end_date)
        else:
            self.set_end_date()

    def set_start_date(self):
        if not self.is_valid_date_range(self.range_select_date, self.end_date):
            self.reset_calendar_date(self.start_date)
            self.date_valid_check = False
            return

        self.start_date = self.range_select_date

    def set_end_date(self):
        if not self.is_valid_date_range(self.start_date, self.range_select_date):
            self.reset_calendar_date(self.end_date)
            self.date_valid_check = False
            return

        self.end_date = self.range_select_date

    def reset_calendar_date(self, new_date):
        self.range_select_date = new_date

    def reset_calendar_today(self):
        self.reset_calendar_date(date.today())

    def reset_date_valid_check(self):
        self.date_valid_check = True

    @rx.var
    def start_year(self) -> int:
        return self.start_date.year

    @rx.var
    def start_month(self) -> int:
        return self.start_date.month

    @rx.var
    def start_day(self) -> int:
        return self.start_date.day

    @rx.var
    def end_year(self) -> int:
        return self.end_date.year

    @rx.var
    def end_month(self) -> int:
        return self.end_date.month

    @rx.var
    def end_day(self) -> int:
        return self.end_date.day

    def is_valid_date_range(self, start: date, end: date):
        return end >= start

    @rx.var(cache=True)
    def data_emotion(self) -> List[str]:
        period_data = self.get_chats_in_period(
            self.start_date,
            self.end_date,
        )
        return [
            message.emotion.value
            for item in period_data
            for message in item.messages
            if message.is_user and message.emotion
        ]

    @rx.var(cache=True)
    def data_emotion_total(self) -> List[str]:
        start_date = date(1970, 1, 1)
        end_date = date(2999, 12, 31)

        total_data = self.get_chats_in_period(
            start_date,
            end_date,
        )
        return [
            message.emotion.value
            for item in total_data
            for message in item.messages
            if message.is_user and message.emotion
        ]

    @rx.var(cache=True)
    def data_emotion_count(self) -> Dict[str, int]:
        emotion_count = {emotion: 0 for emotion in self.emotion_color_map}
        for emotion in self.data_emotion:
            emotion_count[emotion] += 1
        return emotion_count

    @rx.var(cache=True)
    def data_emotion_count_total(self) -> Dict[str, int]:
        emotion_count_total = {emotion: 0 for emotion in self.emotion_color_map}
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
                "기간": period_emotion_count[emotion],
                "전체": total_emotion_count[emotion],
            }
            for emotion in self.emotion_color_map
        ]

    @rx.var
    def data_emotion_funnel(self) -> List[Dict[str, str | int]]:
        data_funnel = [
            {
                "name": emotion,
                "count": count,
                "fill": self.emotion_color_map[emotion],
            }
            for emotion, count in self.data_emotion_count.items()
            if count > 0 and emotion in self.emotion_color_map
        ]
        return sorted(data_funnel, key=lambda x: x["count"], reverse=True)

    @rx.var
    def count_emotions_by_date(self) -> List:
        period_data = self.get_chats_in_period(
            self.start_date,
            self.end_date,
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
            self.start_date,
            self.end_date,
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
