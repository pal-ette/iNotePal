import reflex as rx
import sqlmodel
from .emotion import Emotion


class Color(rx.Model, table=True):
    user_id: str = sqlmodel.Field(
        default=None,
        primary_key=True,
    )

    emotion_colors: str
