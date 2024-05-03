import reflex as rx
from reflex_calendar import calendar
from app.component.chat_input import chat_input
from app.component.chat_history import chat_history, ai_chat_bubble
from app.component.navbar import navbar
from app.state.chat_state import ChatState
from app.component.emotion_card import create_box
from app.page.login import require_login

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


class ModalState(rx.State):
    show: bool = False

    def change(self):
        self.show = not (self.show)


def build_past_card(chat):
    return rx.chakra.button(
        chat[0],
        on_click=lambda: ChatState.select_past_card(chat[1]["id"]),
        bg="#f2ebc8",
        color="#49312d",
    )


@require_login
def dashboard():
    return rx.flex(
        navbar(),
        rx.container(
            margin_top=rx.cond(
                ChatState.has_past_chats,
                "0px",
                "120px",
            ),
        ),
        rx.hstack(
            rx.container(margin_left="120px"),
            rx.spacer(),
            rx.vstack(
                rx.cond(
                    ChatState.has_past_chats,
                    rx.hstack(
                        rx.foreach(
                            ChatState.past_chats,
                            build_past_card,
                        ),
                    ),
                ),
                rx.chakra.heading(
                    ChatState.db_select_date,
                    size="xl",
                    weight="bold",
                    align="center",
                    padding_bottom="2vh",
                ),
                rx.scroll_area(
                    rx.cond(
                        ChatState.is_creating,
                        rx.hstack(
                            rx.chakra.circular_progress(
                                is_indeterminate=ChatState.is_creating
                            ),
                            rx.text("친구가 말 거는 중.."),
                            align="center",
                        ),
                        chat_history(),
                    ),
                    width="100%",
                    min_height="580px",
                ),
                rx.vstack(
                    chat_input(ChatState.is_exist_chat),
                    rx.cond(
                        ChatState.is_closed,
                        rx.hstack(
                            rx.chakra.button(
                                "대화 새로 시작하기",
                                on_click=ChatState.start_new_chat,
                                size="sm",
                                bg="#ebb9b0",
                                color="#49312d",
                                border_radius="md",
                            ),
                        ),
                        rx.cond(
                            ChatState.current_messages.length() > 2,
                            rx.chakra.button(
                                "대화 마치기",
                                on_click=[ChatState.evaluate_chat, ModalState.change],
                                # width="100%",
                                # variant="solid",
                                size="sm",
                                bg="#ebb9b0",
                                color="#49312d",
                                border_radius="md",
                            ),
                        ),
                    ),
                    rx.chakra.modal(
                        rx.chakra.modal_overlay(
                            rx.chakra.modal_content(
                                rx.chakra.modal_header("오늘의 감정"),
                                rx.chakra.modal_body(
                                    rx.flex(create_box())
                                ),  # emotion_card
                                rx.chakra.modal_footer(
                                    rx.chakra.button(
                                        "닫기",
                                        on_click=ModalState.change,
                                    ),
                                ),
                            ),
                        ),
                        # close_on_overlay_click=True,
                        is_centered=True,
                        is_open=ModalState.show,
                    ),
                    # ),
                    align="center",
                    width="100%",
                ),
                height="80vh",
                width="50%",
            ),
            rx.spacer(),
            rx.container(margin_right="120px"),
            height="100%",
            margin="10px",
        ),
        rx.box(flex_grow=1),
        # footer(),
        # align_items="center",
        justify_content="start",
        width="100%",
        height="100%",
        min_height="100vh",
        direction="column",
        # **props,
    )
