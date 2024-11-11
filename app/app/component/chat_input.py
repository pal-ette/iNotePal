import reflex as rx

from app.state.chat_state import ChatState


def chat_input() -> rx.Component:
    return rx.form(
        rx.hstack(
            rx.input(
                placeholder="대화를 입력하세요.",
                id="message",
                width="100%",
                required=True,
                disabled=~ChatState.is_exist_chat,
            ),
            rx.cond(
                ChatState.is_hydrated,
                rx.button(
                    rx.icon("send"),
                    type_="submit",
                    loading=ChatState.is_waiting,
                    disabled=~ChatState.is_exist_chat,
                    variant="outline",
                ),
            ),
            width="100%",
        ),
        on_submit=ChatState.on_submit,
        reset_on_submit=True,
        width="100%",
    )
