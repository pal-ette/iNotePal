# state.py

import os
import reflex as rx
from datetime import datetime
from collections.abc import AsyncGenerator
from openai import OpenAI
from app.app_state import AppState
from app.model.inference_model import InferenceModel
from app.supabase_client import supabase_client
from typing import List, Tuple
from reflex_calendar import reformat_date

inference_model = InferenceModel("dummy-0.0.0")


class ChatState(AppState):
    is_waiting: bool

    input_message: str

    select_date: str = datetime.today().strftime("%a %b %d %Y")

    _db_select_date: str = datetime.today().strftime("%Y-%m-%d")

    _db_chat_id: int

    @rx.cached_var
    def is_closed(self) -> bool:
        if not self.token_is_valid:
            return False

        if not self.is_exist_chat:
            return False

        chat = (
            supabase_client()
            .table("chat")
            .select("is_closed")
            .eq("user_id", self.decodeJWT["sub"])
            .eq("date", self._db_select_date)
            .single()
            .execute()
        )
        return chat.data["is_closed"]

    @rx.cached_var
    def is_exist_chat(self) -> bool:
        if not self.token_is_valid:
            return False

        chat = (
            supabase_client()
            .table("chat")
            .select("*")
            .eq("user_id", self.decodeJWT["sub"])
            .eq("date", self._db_select_date)
            .execute()
        )
        out_is_exist = len(chat.data) > 0
        if out_is_exist:
            self._db_chat_id = chat.data[0]["id"]
        return out_is_exist

    @rx.cached_var
    def chat_history(self) -> List[Tuple[str, str, str]]:
        if not self.is_exist_chat:
            return []
        chats = (
            supabase_client()
            .table("message")
            .select("is_user, message, emotion")
            .eq("chat_id", self._db_chat_id)
            .order("created_at,id", desc=False)
            .execute()
        )
        return [
            (
                "user" if chat_data["is_user"] else "ai",
                chat_data["message"],
                chat_data["emotion"],
            )
            for chat_data in chats.data
        ]

    @rx.cached_var
    def chat_emotion(self) -> str:
        if not self.token_is_valid:
            return ""

        if not self.is_exist_chat:
            return ""

        chat = (
            supabase_client()
            .table("chat")
            .select("emotion")
            .eq("user_id", self.decodeJWT["sub"])
            .eq("date", self._db_select_date)
            .single()
            .execute()
        )
        return chat.data["emotion"]

    def switch_day(self, day):
        self.select_date = day
        self._db_select_date = reformat_date(day)

    def insert_history(self, message, is_user):
        (
            supabase_client()
            .table("message")
            .insert(
                {
                    "chat_id": self._db_chat_id,
                    "message": message,
                    "is_user": is_user,
                }
            )
            .execute()
        )

    def evaluate_chat(self):
        if not self.token_is_valid:
            yield
        (
            supabase_client()
            .table("chat")
            .update(
                {
                    "emotion": "분노",
                    "is_closed": True,
                }
            )
            .eq("id", self._db_chat_id)
            .execute()
        )

    async def start_new_chat(self):
        if not self.token_is_valid:
            yield

        self.is_waiting = True
        yield

        chat = (
            supabase_client()
            .table("chat")
            .insert(
                {
                    "user_id": self.decodeJWT["sub"],
                    "date": self._db_select_date,
                }
            )
            .execute()
        )

        self._db_chat_id = chat.data[0]["id"]

        _y, month, day = self._db_select_date.split("-")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"당신은 심리상담사입니다. 오늘은 {month}월 {day}일 입니다. 오늘 날짜와 함께 오늘 기분이 어땠는지 물어봐줘.",
                }
            ],
            temperature=7e-1,
        )
        self.insert_history(response.choices[0].message.content, is_user=False)
        self.is_waiting = False
        yield

    def set_input_message(self, msg):
        self.input_message = msg

    async def on_submit(self, form_data) -> AsyncGenerator[rx.event.EventSpec]:
        self.is_waiting = True
        yield
        question = form_data["message"]
        self.input_message = ""

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.insert_user_history(question, is_user=True)
        yield

        emotion = inference_model.predict(
            inference_model.padding(
                inference_model.tokenize(
                    [
                        question,
                    ],
                ),
            ),
        )

        yield
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            temperature=7e-1,
        )
        self.insert_history(response.choices[0].message.content, is_user=False)
        self.is_waiting = False
        yield
