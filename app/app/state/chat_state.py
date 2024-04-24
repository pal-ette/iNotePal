# state.py

import os
import reflex as rx
from datetime import datetime
from collections.abc import AsyncGenerator
from openai import OpenAI
from app.app_state import AppState
from app.model.inference_model import InferenceModel
from app.model.roberta7 import Roberta
from app.supabase_client import supabase_client
from typing import List, Tuple, Dict
from reflex_calendar import reformat_date
from reflex import constants


inference_model = InferenceModel("dummy-0.0.0")
env = os.environ.get(constants.ENV_MODE_ENV_VAR)
if env == constants.Env.PROD:
    inference_model = Roberta("model-0.0.1")


class ChatState(AppState):
    is_waiting: bool

    input_message: str

    select_date: str = datetime.today().strftime("%a %b %d %Y")

    _db_select_date: str = datetime.today().strftime("%Y-%m-%d")

    @rx.cached_var
    def current_chat(self) -> Dict:
        if not self.token_is_valid:
            return {}

        response = (
            supabase_client()
            .table("chat")
            .select("*")
            .eq("user_id", self.decodeJWT["sub"])
            .eq("date", self._db_select_date)
            .execute()
        )
        if len(response.data) == 0:
            return {}
        return response.data[0]

    @rx.cached_var
    def current_messages(self) -> List[Tuple[str, str, str]]:
        if not self.is_exist_chat:
            return []
        chats = (
            supabase_client()
            .table("message")
            .select("is_user, message, emotion")
            .eq("chat_id", self.current_chat["id"])
            .order("created_at,id", desc=False)
            .execute()
            .data
        )
        return [
            (
                "user" if chat_data["is_user"] else "ai",
                chat_data["message"],
                chat_data["emotion"],
            )
            for chat_data in chats
        ]

    @rx.var
    def is_closed(self) -> bool:
        if not self.is_exist_chat:
            return False

        return self.current_chat["is_closed"]

    @rx.var
    def is_exist_chat(self) -> bool:
        return bool(self.current_chat)

    @rx.cached_var
    def chat_emotion(self) -> str:
        if not self.is_exist_chat:
            return False

        return self.current_chat["emotion"]

    def switch_day(self, day):
        self.select_date = day
        self._db_select_date = reformat_date(day)

    def insert_history(self, chat_id, message, is_user):
        (
            supabase_client()
            .table("message")
            .insert(
                {
                    "chat_id": chat_id,
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
            .eq("id", self.current_chat["id"])
            .execute()
        )

    async def start_new_chat(self):
        if not self.token_is_valid:
            yield

        self.is_waiting = True
        yield

        new_chat = (
            supabase_client()
            .table("chat")
            .insert(
                {
                    "user_id": self.decodeJWT["sub"],
                    "date": self._db_select_date,
                }
            )
            .execute()
            .data[0]
        )

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
        self.insert_history(
            new_chat["id"],
            response.choices[0].message.content,
            is_user=False,
        )
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
        self.insert_history(self.current_chat["id"], question, is_user=True)
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
        self.insert_history(
            self.current_chat["id"],
            response.choices[0].message.content,
            is_user=False,
        )
        self.is_waiting = False
        yield
