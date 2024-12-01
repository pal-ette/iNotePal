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

    def on_open_change_start_day(self, isOpen):
        if isOpen:
            self.reset_calendar_date(self.start_day)
        else:
            self.set_start_day()

    def on_open_change_end_day(self, isOpen):
        if isOpen:
            self.reset_calendar_date(self.end_day)
        else:
            self.set_end_day()

    def set_start_day(self):
        if not self.is_valid_date_range(self.select_date, self.end_day):
            self.reset_calendar_date(self.start_day)
            self.date_valid_check = False
            return

        self.start_day = self.select_date

    def set_end_day(self):
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
