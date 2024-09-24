import reflex as rx
import sqlmodel
from datetime import datetime as time_type
from typing import Optional
from .emotion import Emotion
from .chat import Chat


class Message(rx.Model, table=True):

    created_at: time_type

    chat_id: int = sqlmodel.Field(foreign_key="chat.id")

    message: str

    is_user: bool

    emotion: Emotion

    chat: Optional["Chat"] = sqlmodel.Relationship(
        back_populates="messages",
    )
