import reflex as rx

from app.state.chat_state import ChatState
from app.schema.chat import Message

shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
chat_margin = "20%"
message_style = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
    display="inline-block",
)

question_style = message_style | dict(
    margin_left=chat_margin,
    background_color=rx.color("gray", 4),
)
answer_style = message_style | dict(
    margin_right=chat_margin,
    background_color="#ebb9b0",
)


def user_chat_bubble(message):
    return rx.vstack(
        rx.hstack(
            rx.text(
                message,
                width="100%",
                text_align="right",
                style=question_style,
            ),
            rx.icon("user"),
            width="100%",
            align="end",
            justify="end",
        ),
        width="100%",
        align="end",
    )


def ai_chat_bubble(message):
    return rx.hstack(
        rx.icon("bot"),
        rx.text(
            message,
            width="100%",
            style=answer_style,
        ),
        width="100%",
        align="start",
    )


def build_chat_bubble(message: Message):
    return rx.cond(
        message.is_user,
        user_chat_bubble(message.message),
        ai_chat_bubble(message.message),
    )


def chat_history() -> rx.Component:
    return rx.foreach(
        ChatState.current_messages,
        build_chat_bubble,
    )
