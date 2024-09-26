import reflex as rx
import sqlmodel
from datetime import date as date_type
from datetime import datetime as time_type
from typing import List, Optional
from .emotion import Emotion


class Chat(rx.Model, table=True):
    date: date_type = sqlmodel.Field(index=True)

    user_id: str = sqlmodel.Field(index=True)  # uuid

    is_closed: bool

    created_at: time_type

    emotion: Emotion

    messages: List["Message"] = sqlmodel.Relationship(
        back_populates="chat",
    )


class Message(rx.Model, table=True):

    created_at: time_type

    chat_id: int = sqlmodel.Field(foreign_key="chat.id")

    message: str

    is_user: bool

    emotion: Emotion

    chat: Optional["Chat"] = sqlmodel.Relationship(
        back_populates="messages",
    )
