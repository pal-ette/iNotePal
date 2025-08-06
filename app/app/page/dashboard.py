import reflex as rx
import reflex_local_auth

from app.component.chat_input import chat_input
from app.component.chat_history import chat_history
from app.component.navbar import navbar
from app.state.chat_state import ChatState
from app.component.emotion_card import create_box
from app.state.calendar_state import calendar_component
from app.routes import DASHBOARD_ROUTE
from typing import Tuple
from app.schema.chat import Chat

# 그래프 그리기 위한 임시 데이터.
data = [
    {"name": "4/1", "pos": 4, "neg": 6, "neu": 0},
    {"name": "4/2", "pos": 5, "neg": 3, "neu": 0},
    {"name": "4/3", "pos": 3, "neg": 1, "neu": 0},
    {"name": "4/4", "pos": 1, "neg": 2, "neu": 3},
    {"name": "4/5", "pos": 2, "neg": 2, "neu": 3},
    {"name": "4/6", "pos": 0, "neg": 2, "neu": 2},
    {"name": "4/7", "pos": 3, "neg": 1, "neu": 1},
]


def build_past_card(chat: Tuple[int, Chat]):
    return rx.button(
        chat[0],
        on_click=lambda: ChatState.select_past_card(chat[1]["id"]),
        bg=rx.cond(
            ChatState.current_chat["id"] == chat[1]["id"],
            rx.color_mode_cond(
                light="#ebb9b0",
                dark="#af625c",
            ),
            "#f2ebc8",
        ),
        color=rx.cond(
            ChatState.current_chat["id"] == chat[1]["id"],
            "currentColor",
            "#49312d",
        ),
    )


@rx.page(
    route=DASHBOARD_ROUTE,
    on_load=[
        ChatState.on_load,
        ChatState.on_load_dashboard,
    ],
)
@reflex_local_auth.require_login
def dashboard():
    return rx.flex(
        navbar(),
        rx.hstack(
            rx.vstack(
                rx.container(
                    height="50px",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon(
                            tag="chevron_left",
                        ),
                        variant="ghost",
                        on_click=ChatState.select_prev_date,
                        disabled=~ChatState.can_prev_date,
                    ),
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                rx.heading(
                                    ChatState.print_date_text,
                                    size="6",
                                    weight="bold",
                                    align="center",
                                    high_contrast=True,
                                ),
                                variant="ghost",
                            ),
                        ),
                        rx.popover.content(
                            calendar_component(
                                rx.hstack(
                                    rx.popover.close(
                                        rx.button(
                                            "닫기",
                                            size="1",
                                            color_scheme="tomato",
                                        ),
                                    ),
                                ),
                                select_date=ChatState.select_date,
                                accent_dates=ChatState.dates_has_closed_chat,
                                on_change_date=ChatState.on_change_date,
                                allow_future=False,
                            ),
                        ),
                    ),
                    rx.button(
                        rx.icon(
                            tag="chevron_right",
                        ),
                        variant="ghost",
                        on_click=ChatState.select_next_date,
                        disabled=~ChatState.can_next_date,
                    ),
                    rx.scroll_area(
                        rx.hstack(
                            rx.foreach(
                                ChatState.past_chats,
                                build_past_card,
                            ),
                        ),
                        width="300px",
                    ),
                    class_name="items-center",
                ),
                rx.scroll_area(
                    rx.cond(
                        ChatState.is_creating,
                        rx.hstack(
                            rx.spinner(loading=ChatState.is_creating),
                            rx.text("친구가 말 거는 중.."),
                            align="center",
                        ),
                        rx.vstack(
                            chat_history(),
                        ),
                    ),
                    width="100%",
                    id="chat_area",
                    margin_bottom="120px",
                ),
                rx.vstack(
                    rx.cond(
                        ~ChatState.is_closed,
                        chat_input(),
                    ),
                    rx.hstack(
                        rx.button(
                            "대화 새로 시작하기",
                            on_click=ChatState.start_new_chat,
                            size="2",
                            border_radius="md",
                            disabled=(
                                ChatState.is_creating | ChatState.is_latest_chat_opened
                            ),
                        ),
                        rx.button(
                            "대화 마치기",
                            on_click=ChatState.evaluate_chat,
                            size="2",
                            border_radius="md",
                            disabled=(
                                ChatState.is_creating
                                | ChatState.is_closed
                                | (ChatState.current_messages.length() < 3)
                            ),
                        ),
                    ),
                    rx.dialog.root(
                        rx.dialog.content(
                            rx.heading("오늘의 감정"),
                            rx.flex(create_box()),
                            rx.button(
                                "닫기",
                                on_click=ChatState.close_result_modal,
                            ),
                        ),
                        # close_on_overlay_click=True,
                        is_centered=True,
                        open=ChatState.show_result_modal,
                    ),
                    align="center",
                    width="100%",
                    class_name="absolute bottom-8",
                ),
                height="100vh",
                class_name="relative mx-10",
            ),
            align_items="center",
        ),
        align_items="center",
        justify_content="start",
        width="100%",
        height="100%",
        min_height="100vh",
        direction="column",
    )
