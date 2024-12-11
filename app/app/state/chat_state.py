# state.py

import os
import reflex as rx
from datetime import date
from openai import OpenAI
from app.app_state import AppState
from app.model.inference_model import InferenceModel
from app.model.embedding_model import EmbeddingModel
from app.model.roberta import Roberta
from app.schema.greeting import Greeting
from app.schema.chat import Chat, Message
from app.schema.color import Color
from app.schema.emotion import Emotion
from app.util.emotion import emotion_color_map_default
from app.supabase_client import supabase_client
from typing import List, Tuple, Dict
from reflex import constants
import random
from collections import Counter
import sqlalchemy
from reflex.config import environment


inference_model = InferenceModel("dummy-0.0.0")
embedding_model = None
env = environment.REFLEX_ENV_MODE.get()
if env == constants.Env.PROD:
    inference_model = Roberta("model-0.0.2")
    embedding_model = EmbeddingModel("")
# elif env == constants.Env.DEV:
#     embedding_model = EmbeddingModel("")


class ChatState(AppState):
    is_waiting: bool = False

    select_date: date = date.today()

    is_creating: bool

    show_result_modal: bool = False

    _current_chat_index: int = 0

    _db_chats: Dict[str, List[Chat]] = {}

    _db_messages: Dict[int, List[Message]] = {}

    @rx.var(cache=True)
    def db_select_date(self) -> str:
        return str(self.select_date)

    @rx.var(cache=True)
    def chats(self) -> List[Chat]:
        if self.db_select_date in self._db_chats:
            return self._db_chats[self.db_select_date]

        if not self.token_is_valid:
            return []

        chats: List[Chat] = []

        with rx.session() as session:
            chats = session.exec(
                Chat.select()
                .where(Chat.user_id == self.user_id)
                .where(Chat.date == self.db_select_date)
                .order_by(Chat.id)
            ).all()

        if len(chats) == 0:
            return []
        self._db_chats[self.db_select_date] = chats
        return self._db_chats[self.db_select_date]

    @rx.var()
    def dates_has_closed_chat(self) -> List[date]:
        dates = []
        with rx.session() as session:
            dates = [
                chat.date
                for chat in session.exec(
                    Chat.select()
                    .where(Chat.user_id == self.user_id)
                    .where(Chat.is_closed)
                ).all()
            ]
        return dates

    @rx.var(cache=True)
    def past_chats(self) -> List[Tuple[int, Chat]]:
        return [
            (len(self.chats) - i, chat) if chat.is_closed else ("현재 대화", chat)
            for i, chat in enumerate(self.chats)
            # if i != self._current_chat_index
        ]

    @rx.var(cache=True)
    def past_messages(self) -> List[Tuple[str, str, str]]:
        return [
            (chat.id, self.get_messages(chat.id))
            for i, chat in enumerate(self.chats)
            if chat.is_closed
        ]

    @rx.var(cache=True)
    def has_past_chats(self) -> bool:
        return len(self.past_chats) > 1

    @rx.var(cache=True)
    def current_chat(self) -> Chat | None:
        chats = self.chats
        if len(chats) < 1:
            return None
        return chats[self._current_chat_index]

    @rx.var(cache=True)
    def current_messages(self) -> List[Message]:
        if not self.current_chat:
            return []
        return self.get_messages(self.current_chat.id)

    @rx.var(cache=True)
    def is_closed(self) -> bool:
        if not self.is_exist_chat:
            return False
        return self.current_chat.is_closed

    @rx.var(cache=True)
    def is_latest_chat_opened(self) -> bool:
        if not self.is_exist_chat:
            return False
        return not self.chats[0].is_closed

    @rx.var(cache=True)
    def is_exist_chat(self) -> bool:
        return bool(self.current_chat)

    def on_change_date(self, year, month, day):
        self.select_date = date(year, month, day)

        self._current_chat_index = 0

        if len(self.chats) == 0:
            yield ChatState.start_new_chat

        return ChatState.scroll_to_bottom

    def get_chats_in_period(self, start_day, end_day) -> List[Chat]:
        chats = []
        if not self.token_is_valid:
            return chats

        with rx.session() as session:
            chats = session.exec(
                Chat.select()
                .options(
                    sqlalchemy.orm.selectinload(Chat.messages),
                )
                .where(Chat.user_id == self.user_id)
                .where(Chat.date >= start_day)
                .where(Chat.date <= end_day)
                .order_by(Chat.id)
            ).all()

        return chats

    @rx.var(cache=True)
    def print_date_text(self) -> str:
        year = self.select_date.year
        month = self.select_date.month
        day = self.select_date.day
        return f"{year}년 {month}월 {day}일"

    @rx.var
    def emotion_color_map(self) -> Dict[str, str]:
        color_map = emotion_color_map_default

        with rx.session() as session:
            user_color_str = session.exec(
                Color.select().where(Color.user_id == self.user_id)
            ).one_or_none()
            if user_color_str:
                user_color_list = user_color_str.split(",")
                for i, emotion in enumerate(color_map):
                    color_map[emotion] = user_color_list[i]

        return color_map

    def get_messages(self, chat_id):
        if chat_id in self._db_messages:
            # print("get_messages", self._db_messages[chat_id])
            return self._db_messages[chat_id]
        messages: List[Message] = []

        with rx.session() as session:
            messages = session.exec(
                Message.select()
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at, Message.id)
            ).all()

        self._db_messages[chat_id] = messages
        return self._db_messages[chat_id]

    def select_past_card(self, chat_id):
        if self.current_chat and self.current_chat.id == chat_id:
            return
        for i, chat in enumerate(self.chats):
            if chat.id != chat_id:
                continue
            self._current_chat_index = i
            break

        yield ChatState.scroll_to_bottom

    def insert_history(self, chat_id, message, is_user, emotion=None):
        new_message = Message(
            chat_id=chat_id,
            message=message,
            is_user=is_user,
            emotion=Emotion[emotion] if emotion else emotion,
        )
        with rx.session() as session:
            session.add(new_message)
            session.commit()

            session.refresh(new_message)

        if chat_id in self._db_messages:
            self._db_messages[chat_id].append(new_message)
        else:
            self._db_messages[chat_id] = [new_message]

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
                message.emotion.value
                for message in self.current_messages
                if message.is_user
            ]
        ).most_common(1)
        return emotion

    def evaluate_chat(self):
        emotion = self.select_current_chat_emotion()

        date_key = str(self.current_chat.date)
        for i, chat in enumerate(self._db_chats[date_key]):
            if chat.id != self.current_chat.id:
                continue

            with rx.session() as session:
                chat.set(
                    emotion=emotion,
                    is_closed=True,
                )
                session.add(chat)
                session.commit()
                session.refresh(chat)

            self._db_chats[date_key][i] = chat

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
        month = self.select_date.month
        day = self.select_date.day
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"당신은 사람의 감정을 세심히 살필 수 있는 심리상담사입니다. 오늘은 {month}월 {day}일 입니다. 기분이라는 단어를 직접적으로 사용하지말고 오늘 날짜와 함께 기분이 드러날 수 있는 질문을 해주세요.",
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

    def start_new_chat(self):
        if not self.is_hydrated:
            return ChatState.start_new_chat()

        self.is_creating = True
        yield

        new_chat = Chat(
            user_id=self.user_id,
            date=self.db_select_date,
        )

        with rx.session() as session:
            session.add(new_chat)
            session.commit()

            session.refresh(new_chat)

        if not new_chat:
            print("error start new chat")
            self.is_creating = False
            return

        if self.db_select_date in self._db_chats:
            self._db_chats[self.db_select_date].insert(0, new_chat)
        else:
            self._db_chats[self.db_select_date] = [new_chat]

        self._current_chat_index = 0

        greeting = self.get_greeting()
        self.insert_history(
            new_chat.id,
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

    def on_load_dashboard(self):
        if not self.is_hydrated:
            return ChatState.on_load_dashboard()

        if self.is_exist_chat:
            return

        if len(self.chats) > 0:
            return

        return ChatState.start_new_chat()

    def on_submit(self, form_data):
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
            self.current_chat.id,
            question,
            is_user=True,
            emotion=emotion,
        )
        yield

        response = self._talk_to_embed_db(question)
        if response is None:
            response = self._talk_to_open_ai(question)

        self.insert_history(
            self.current_chat.id,
            response,
            is_user=False,
        )
        self.is_waiting = False
        yield self.scroll_to_bottom()
