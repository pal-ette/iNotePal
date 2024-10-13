import reflex as rx

from app.component.chat_input import chat_input
from app.component.chat_history import chat_history, ai_chat_bubble
from app.component.navbar import navbar
from app.state.chat_state import ChatState
from app.component.emotion_card import create_box, emotion_card, show_emotion_colors
from app.page.login import require_login
from app.state.calendar_state import calendar_component

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


def build_past_card(chat):
    return rx.button(
        chat[0],
        on_click=lambda: ChatState.select_past_card(chat[1]["id"]),
        bg=rx.cond(
            ChatState.current_chat["id"] == chat[1]["id"],
            "#e5988e",
            "#f2ebc8",
        ),
        color="#49312d",
    )


@require_login
def dashboard():
    return rx.flex(
        navbar(),
        rx.container(
            margin_top="30px",
        ),
        rx.hstack(
            rx.container(
                rx.grid(
                    rx.vstack(
                        calendar_component(
                            year=ChatState.year,
                            select_year=ChatState.select_year,
                            month=ChatState.month,
                            select_month=ChatState.select_month,
                            day=ChatState.day,
                            on_next_month=ChatState.on_next_month,
                            on_prev_month=ChatState.on_prev_month,
                            on_change_day=ChatState.on_change_day,
                        ),
                        rx.text(
                            f"{ChatState.print_date_text}의 감정",
                            # on_change=State.select_date,
                            as_="i",
                            font_size="1.5em",
                            weight="bold",
                        ),
                        show_emotion_colors(),
                        emotion_card(),
                        display=["none", "none", "none", "none", "flex", "flex"],
                    ),
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
                        rx.heading(
                            ChatState.print_date_text,
                            size="xl",
                            weight="bold",
                            align="center",
                            padding_bottom="2vh",
                        ),
                        rx.scroll_area(
                            rx.cond(
                                ChatState.is_creating,
                                rx.hstack(
                                    rx.spinner(loading=ChatState.is_creating),
                                    rx.text("친구가 말 거는 중.."),
                                    align="center",
                                ),
                                chat_history(),
                            ),
                            width="100%",
                            min_height="500px",
                            id="chat_area",
                        ),
                        rx.vstack(
                            chat_input(ChatState.is_exist_chat),
                            rx.cond(
                                ~ChatState.is_creating,
                                rx.cond(
                                    ~ChatState.is_exist_chat | ChatState.is_closed,
                                    rx.hstack(
                                        rx.button(
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
                                        rx.button(
                                            "대화 마치기",
                                            on_click=ChatState.evaluate_chat,
                                            # width="100%",
                                            # variant="solid",
                                            size="sm",
                                            bg="#ebb9b0",
                                            color="#49312d",
                                            border_radius="md",
                                        ),
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
                        ),
                        height="80vh",
                        width="100%",
                    ),
                    width="100%",
                    grid_template_columns=[
                        "repeat(1, 1fr)",
                        "repeat(1, 1fr)",
                        "repeat(1, 1fr)",
                        "repeat(1, 1fr)",
                        "repeat(2, 1fr)",
                        "repeat(2, 1fr)",
                    ],
                ),
                width=["688px", "688px", "688px", "688px", "1136px", "1136px"],
                max_width=["none", "none", "none", "none", "none", "none"],
            ),
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
