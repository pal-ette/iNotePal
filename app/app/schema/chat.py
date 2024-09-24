import reflex as rx
import sqlmodel
from datetime import date as date_type
from datetime import datetime as time_type
from .emotion import Emotion


class Chat(rx.Model, table=True):
    date: date_type = sqlmodel.Field(index=True)

    user_id: str = sqlmodel.Field(index=True)  # uuid

    is_closed: bool

    created_at: time_type

    emotion: Emotion
