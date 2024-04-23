import reflex as rx

from app.state.chat_state import ChatState


def user_chat_bubble(message, emotion):
    return rx.hstack(
        rx.text(
            message,
            width="100%",
            text_align="right",
        ),
        rx.icon("user"),
        width="100%",
        align="end",
    )


def ai_chat_bubble(message, emotion):
    return rx.hstack(
        rx.icon("bot"),
        rx.text(
            message,
            width="100%",
        ),
        width="100%",
        align="start",
    )


def build_chat_bubble(chat):
    return rx.cond(
        chat[0] == "user",
        user_chat_bubble(chat[1], chat[2]),
        ai_chat_bubble(chat[1], chat[2]),
    )


def chat_history() -> rx.Component:
    return rx.foreach(
        ChatState.current_messages,
        build_chat_bubble,
    )
