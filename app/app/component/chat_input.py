import reflex as rx
import reflex_chakra as rc

from app.state.chat_state import ChatState


def chat_input(can_input: bool) -> rx.Component:
    return rc.form(
        rx.hstack(
            rc.input(
                placeholder="대화를 입력하세요.",
                id="message",
                width="100%",
                is_required=True,
                is_disabled=~can_input,
            ),
            rx.cond(
                ChatState.is_hydrated,
                rc.button(
                    rx.icon("send"),
                    type_="submit",
                    is_loading=ChatState.is_waiting,
                    is_disabled=~can_input,
                    variant="outline",
                ),
            ),
            width="100%",
        ),
        on_submit=ChatState.on_submit,
        on_mount=ChatState.on_mount,
        reset_on_submit=True,
        width="100%",
    )
