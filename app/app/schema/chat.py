import reflex as rx
from datetime import date as date_type
from datetime import datetime as time_type
from enum import Enum


class Emotion(Enum):
    공포 = 1
    기쁨 = 2
    놀람 = 3
    분노 = 4
    슬픔 = 5
    중립 = 6
    혐오 = 7


class Chat(rx.Model, table=True):
    date: date_type

    user_id: str  # uuid

    is_closed: bool

    created_at: time_type

    emotion: Emotion
