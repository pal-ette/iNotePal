import reflex as rx
from reflex_calendar import calendar
from app.component.chat_input import chat_input
from app.component.chat_history import chat_history
from app.component.navbar import navbar
from app.state.chat_state import ChatState
from app.page.login import require_login


@require_login
def dashboard():
    return rx.flex(
        navbar(),
        rx.container(
            margin_top="70px",
        ),
        rx.hstack(
            rx.vstack(
                calendar(
                    locale="ko-KR",
                    width="100%",
                    on_change=ChatState.switch_day,
                    value=ChatState.select_date,
                ),
                rx.card(
                    "graph",
                    width="100%",
                    height="100%",
                ),
                width="50%",
            ),
            rx.vstack(
                rx.cond(
                    ~ChatState.is_exist_chat,
                    rx.flex(
                        rx.button(
                            "새로운 대화를 시작할까요?",
                            on_click=ChatState.start_new_chat,
                            disabled=ChatState.is_waiting,
                        ),
                        align="center",
                        height="800px",
                        width="100%",
                        justify="center",
                    ),
                    rx.scroll_area(
                        rx.vstack(
                            chat_history(),
                            rx.cond(
                                ChatState.is_closed,
                                rx.badge(
                                    ChatState.chat_emotion,
                                ),
                                rx.button(
                                    "대화 마치기",
                                    on_click=ChatState.evaluate_chat,
                                ),
                            ),
                            align="center",
                            width="100%",
                        ),
                        width="100%",
                        height="800px",
                    ),
                ),
                chat_input(ChatState.is_exist_chat),
                height="100%",
                width="50%",
            ),
            height="100%",
            margin="10px",
        ),
        rx.box(flex_grow=1),
        # footer(),
        align_items="center",
        justify_content="start",
        width="100%",
        height="100%",
        min_height="100vh",
        direction="column",
        # **props,
    )
    return rx.vstack(
        navbar(),
        rx.container(
            height="70px",
        ),
        height="100vh",
    )
