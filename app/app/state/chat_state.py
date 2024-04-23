# state.py

import os
import reflex as rx
from datetime import datetime
from collections.abc import AsyncGenerator
from openai import AsyncOpenAI
from app.app_state import AppState
from app.model.inference_model import InferenceModel
from app.supabase_client import supabase_client

inference_model = InferenceModel("dummy-0.0.0")


class ChatState(AppState):
    is_waiting: bool

    input_message: str

    select_date: str = datetime.today().strftime("%Y-%m-%d")

    chat_history: list[tuple[str, str]]

    _db_chat_id: int

    @rx.cached_var
    def is_selected_today(self):
        return self.select_date == datetime.today().strftime("%Y-%m-%d")

    @rx.cached_var
    def is_exist_chat(self):
        if not self.token_is_valid:
            return False

        user = supabase_client().auth.get_user(self.auth_token)
        chat = (
            supabase_client()
            .table("chat")
            .select("*")
            .eq("user_id", user.user.id)
            .eq("date", self.select_date)
            .execute()
        )
        out_is_exist = len(chat.data) > 0
        if out_is_exist:
            self._db_chat_id = chat.data[0]["id"]
        return out_is_exist

    def switch_day(self, day):
        self.select_date = datetime.strptime(day, "%a %b %d %Y").strftime("%Y-%m-%d")

        if self.is_exist_chat:
            chats = (
                supabase_client()
                .table("message")
                .select("is_user, message")
                .eq("chat_id", self._db_chat_id)
                .order("created_at,id", desc=False)
                .execute()
            )
            self.chat_history = [
                ("user" if chat_data["is_user"] else "ai", chat_data["message"])
                for chat_data in chats.data
            ]

    def insert_user_history(self, message):
        user = supabase_client().auth.get_user(self.auth_token)
        (
            supabase_client()
            .table("message")
            .insert(
                {
                    "chat_id": self._db_chat_id,
                    "message": message,
                    "is_user": True,
                }
            )
            .execute()
        )

    def insert_bot_history(self, message):
        user = supabase_client().auth.get_user(self.auth_token)
        (
            supabase_client()
            .table("message")
            .insert(
                {
                    "chat_id": self._db_chat_id,
                    "message": message,
                    "is_user": False,
                }
            )
            .execute()
        )

    async def start_new_chat(self):
        if not self.token_is_valid:
            yield

        self.is_waiting = True
        yield

        user = supabase_client().auth.get_user(self.auth_token)
        chat = (
            supabase_client()
            .table("chat")
            .insert(
                {
                    "user_id": user.user.id,
                    "date": self.select_date,
                }
            )
            .execute()
        )

        self._db_chat_id = chat.data[0]["id"]

        _y, month, day = self.select_date.split("-")
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        session = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"당신은 심리상담사입니다. 오늘은 {month}월 {day}일 입니다. 오늘 날짜와 함께 오늘 기분이 어땠는지 물어봐줘.",
                }
            ],
            stop=None,
            temperature=7e-1,
            stream=True,
        )
        self.chat_history.append(("ai", ""))
        answer = ""
        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = ("ai", answer)
                yield
        self.insert_bot_history(self.chat_history[-1][1])
        self.is_waiting = False
        yield

    def set_input_message(self, msg):
        self.input_message = msg

    async def on_submit(self, form_data) -> AsyncGenerator[rx.event.EventSpec]:
        self.is_waiting = True
        question = form_data["message"]
        self.input_message = ""

        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        session = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            stop=None,
            temperature=7e-1,
            stream=True,
        )
        emote = inference_model.predict(
            inference_model.padding(
                inference_model.tokenize(
                    [
                        question,
                    ],
                ),
            ),
        )

        self.chat_history.append(("user", question))
        self.insert_user_history(self.chat_history[-1][1])

        self.chat_history.append(("ai", ""))
        answer = ""
        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = ("ai", answer)
                yield
        self.insert_bot_history(self.chat_history[-1][1])
        self.is_waiting = False
        yield
