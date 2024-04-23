import reflex as rx

from app.state.chat_state import ChatState


def chat_input() -> rx.Component:
    return rx.chakra.form(
        rx.hstack(
            rx.chakra.input(
                placeholder="문자를 입력하세요.",
                id="message",
                width="100%",
                value=ChatState.input_message,
                on_change=ChatState.set_input_message,
                is_required=True,
            ),
            rx.cond(
                ChatState.is_hydrated,
                rx.chakra.button(
                    "보내기",
                    type_="submit",
                    is_loading=ChatState.is_waiting,
                ),
            ),
            width="100%",
        ),
        on_submit=ChatState.on_submit,
        width="100%",
    )
