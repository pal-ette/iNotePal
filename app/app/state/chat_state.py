# state.py

import os
import reflex as rx
from datetime import datetime, date
from collections.abc import AsyncGenerator
from openai import OpenAI
from app.app_state import AppState
from app.model.inference_model import InferenceModel
from app.model.embedding_model import EmbeddingModel
from app.model.roberta import Roberta
from app.schema.greeting import Greeting
from app.supabase_client import supabase_client
from typing import List, Tuple, Dict
from reflex import constants
import random
from collections import Counter


inference_model = InferenceModel("dummy-0.0.0")
embedding_model = None
env = os.environ.get(constants.ENV_MODE_ENV_VAR)
if env == constants.Env.PROD:
    inference_model = Roberta("model-0.0.2")
    embedding_model = EmbeddingModel("")
# elif env == constants.Env.DEV:
#     embedding_model = EmbeddingModel("")


class ChatState(AppState):
    is_waiting: bool = False

    year: int = datetime.now().year
    month: int = datetime.now().month
    day: int = datetime.now().day

    select_year: int = datetime.now().year
    select_month: int = datetime.now().month

    is_creating: bool

    show_result_modal: bool = False

    _current_chat_index: int = 0

    _db_chats: Dict[str, List[Dict[str, str]]] = {}

    _db_messages: Dict[int, List[Tuple[str, str, str]]] = {}

    @rx.var(cache=True)
    def db_select_date(self):
        return str(date(self.select_year, self.select_month, self.day))

    @rx.var(cache=True)
    def chats(self) -> List:
        if self.db_select_date in self._db_chats:
            return self._db_chats[self.db_select_date]

        if not self.token_is_valid:
            return []

        response = (
            supabase_client()
            .table("chat")
            .select("*")
            .eq("user_id", self.decodeJWT["sub"])
            .eq("date", self.db_select_date)
            .order("id", desc=True)
            .execute()
        )
        if len(response.data) == 0:
            return []
        self._db_chats[self.db_select_date] = response.data
        return self._db_chats[self.db_select_date]

    @rx.var(cache=True)
    def past_chats(self) -> List[Tuple[int, Dict[str, str]]]:
        return [
            (len(self.chats) - i, chat) if chat["is_closed"] else ("현재 대화", chat)
            for i, chat in enumerate(self.chats)
            # if i != self._current_chat_index
        ][::-1]

    @rx.var(cache=True)
    def past_messages(self) -> List[Tuple[str, str, str]]:
        return [
            (chat["id"], self.get_messages(chat["id"]))
            for i, chat in enumerate(self.chats)
            if chat["is_closed"]
        ]

    @rx.var(cache=True)
    def has_past_chats(self) -> bool:
        return len(self.past_chats) > 1

    @rx.var(cache=True)
    def current_chat(self) -> Dict[str, str]:
        chats = self.chats
        if len(chats) < 1:
            return {}
        return chats[self._current_chat_index]

    @rx.var(cache=True)
    def current_messages(self) -> List[Tuple[str, str, str]]:
        if not self.current_chat:
            return []
        return self.get_messages(self.current_chat["id"])

    @rx.var(cache=True)
    def is_closed(self) -> bool:
        if not self.is_exist_chat:
            return False
        return self.current_chat["is_closed"]

    @rx.var(cache=True)
    def is_exist_chat(self) -> bool:
        return bool(self.current_chat)

    @rx.var(cache=True)
    def chat_emotion(self) -> str:
        if not self.is_exist_chat:
            return False

        return self.current_chat["emotion"]

    def on_next_month(self):
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1

    def on_prev_month(self):
        if self.month == 1:
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1

    def on_change_day(self, day):
        self.select_year = self.year
        self.select_month = self.month
        self.day = day
        self._current_chat_index = 0

        if len(self.chats) == 0:
            return self.start_new_chat()

    def get_chats_in_period(self, start_day, end_day):
        if not self.token_is_valid:
            return []
        return (
            supabase_client()
            .table("chat")
            .select("*, message(*)")
            .eq("user_id", self.decodeJWT["sub"])
            .gte("date", start_day)
            .lte("date", end_day)
            .order("id", desc=True)
            .execute()
            .data
        )

    @rx.var(cache=True)
    def print_date_text(self):
        return f"{self.select_year}년 {self.select_month}월 {self.day}일"

    def get_messages(self, chat_id):
        if chat_id in self._db_messages:
            # print("get_messages", self._db_messages[chat_id])
            return self._db_messages[chat_id]
        messages = (
            supabase_client()
            .table("message")
            .select("is_user, message, emotion")
            .eq("chat_id", chat_id)
            .order("created_at,id", desc=False)
            .execute()
            .data
        )
        self._db_messages[chat_id] = [
            (
                "user" if chat_data["is_user"] else "ai",
                chat_data["message"],
                chat_data["emotion"],
            )
            for chat_data in messages
        ]
        return self._db_messages[chat_id]

    def select_past_card(self, chat_id):
        if self.current_chat and self.current_chat["id"] == chat_id:
            return
        for i, chat in enumerate(self.chats):
            if chat["id"] != chat_id:
                continue
            self._current_chat_index = i
            break

    def insert_history(self, chat_id, message, is_user, emotion=None):
        (
            supabase_client()
            .table("message")
            .insert(
                {
                    "chat_id": chat_id,
                    "message": message,
                    "is_user": is_user,
                    "emotion": emotion,
                }
            )
            .execute()
        )
        cache_item = ("user" if is_user else "ai", message, emotion)
        if chat_id in self._db_messages:
            self._db_messages[chat_id].append(cache_item)
        else:
            self._db_messages[chat_id] = [cache_item]

    def scroll_to_bottom(self):
        return rx.call_script(
            """
            var element = document.getElementById('chat_area');
            element.scrollTop = element.scrollHeight;
            """
        )

    def select_current_chat_emotion(self):
        [(emotion, _count)] = Counter(
            [
                emotion
                for type, message, emotion in self.current_messages
                if type == "user"
            ]
        ).most_common(1)
        return emotion

    def evaluate_chat(self):
        new_data = {
            "emotion": self.select_current_chat_emotion(),
            "is_closed": True,
        }
        (
            supabase_client()
            .table("chat")
            .update(new_data)
            .eq("id", self.current_chat["id"])
            .execute()
            .data[0]
        )

        def update_chat(chat):
            if chat["id"] != self.current_chat["id"]:
                return chat
            return self.current_chat | new_data

        self._db_chats[self.current_chat["date"]] = list(
            map(
                update_chat,
                self._db_chats[self.current_chat["date"]],
            ),
        )
        self.open_result_modal()

    def open_result_modal(self):
        if self.show_result_modal:
            return

        self.show_result_modal = True

    def close_result_modal(self):
        if not self.show_result_modal:
            return

        self.show_result_modal = False

    def get_greeting(self):
        greeting = None
        with rx.session() as session:
            greeting = session.exec(
                Greeting.select().where(Greeting.date == self.db_select_date)
            ).one_or_none()

        if greeting is not None:
            return greeting.message

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"당신은 사람의 감정을 세심히 살필 수 있는 심리상담사입니다. 오늘은 {self.select_month}월 {self.day}일 입니다. 기분이라는 단어를 직접적으로 사용하지말고 오늘 날짜와 함께 기분이 드러날 수 있는 질문을 해주세요.",
                }
            ],
            temperature=7e-1,
        )
        out_greeting = response.choices[0].message.content
        with rx.session() as session:
            session.add(
                Greeting(
                    date=self.db_select_date,
                    message=out_greeting,
                ),
            )
            session.commit()

        return out_greeting

    async def start_new_chat(self):
        if not self.is_hydrated:
            return

        self.is_creating = True
        yield

        new_chat = (
            supabase_client()
            .table("chat")
            .insert(
                {
                    "user_id": self.decodeJWT["sub"],
                    "date": self.db_select_date,
                }
            )
            .execute()
            .data[0]
        )

        if self.db_select_date not in self._db_chats:
            self._db_chats[self.db_select_date] = [new_chat]
        else:
            self._db_chats[self.db_select_date].insert(0, new_chat)

        greeting = self.get_greeting()
        self.insert_history(
            new_chat["id"],
            greeting,
            is_user=False,
        )
        self.is_creating = False

    def _talk_to_open_ai(self, message):
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        response = (
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": message}],
                temperature=7e-1,
            )
            .choices[0]
            .message.content
        )
        return response

    def _talk_to_embed_db(self, message):
        if embedding_model is None:
            return None
        embedding = embedding_model.predict(message)
        response = random.sample(
            supabase_client()
            .rpc(
                "match_sentences",
                {
                    "query_embedding": str(embedding.tolist()),
                    "match_threshold": 0.0,
                    "match_count": 3,
                },
            )
            .execute()
            .data,
            1,
        )[0]["content"]

        return response

    def on_mount(self):
        if not self.is_hydrated:
            return

        if self.is_exist_chat:
            return

        if len(self.chats) == 0:
            return self.start_new_chat()

    async def on_submit(self, form_data) -> AsyncGenerator[rx.event.EventSpec]:
        self.is_waiting = True
        yield
        question = form_data["message"]

        emotion = inference_model.predict(
            inference_model.padding(
                inference_model.tokenize(
                    question,
                ),
            ),
        )

        self.insert_history(
            self.current_chat["id"],
            question,
            is_user=True,
            emotion=emotion,
        )
        yield

        response = self._talk_to_embed_db(question)
        if response is None:
            response = self._talk_to_open_ai(question)

        self.insert_history(
            self.current_chat["id"],
            response,
            is_user=False,
        )
        self.is_waiting = False
        yield self.scroll_to_bottom()
