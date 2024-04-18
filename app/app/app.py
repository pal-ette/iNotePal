"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from app import style
from app.state import State
from dotenv import load_dotenv

# 외부 정의 DB 모델

load_dotenv()


def qa(question: str, answer: str) -> rx.Component:
    return rx.chakra.box(
        rx.chakra.box(
            rx.chakra.text(
                question,
                text_align="right",
            ),
            style=style.question_style,
        ),
        rx.chakra.box(
            rx.chakra.text(
                answer,
                text_align="left",
            ),
            style=style.answer_style,
        ),
    )


def chat() -> rx.Component:
    return rx.chakra.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(
                messages[0],
                messages[1],
            ),
        )
    )


def action_bar() -> rx.Component:
    return rx.chakra.hstack(
        rx.chakra.input(
            value=State.question,
            placeholder="Ask a question",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.chakra.button(
            "Ask",
            on_click=State.answer,
            style=style.button_style,
        ),
    )


def index() -> rx.Component:
    return rx.chakra.center(
        rx.chakra.vstack(
            chat(),
            action_bar(),
            align="center",
        ),
    )


app = rx.App()
app.add_page(index)
