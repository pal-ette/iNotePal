import reflex as rx
from reflex_calendar import calendar
from app.component.chat_input import chat_input
from app.component.chat_history import chat_history
from app.component.navbar import navbar
from app.state.chat_state import ChatState
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


@require_login
def dashboard():
    return rx.flex(
        navbar(),
        rx.container(
            margin_top="120px",
        ),
        rx.hstack(
            rx.vstack(
                calendar(
                    locale="ko-KR",
                    width="100%",
                    on_change=ChatState.switch_day,
                    value=ChatState.select_date,
                ),
                rx.flex(
                    rx.link(
                        rx.recharts.bar_chart(
                            rx.recharts.bar(
                                data_key="pos", stroke="#8884d8", fill="#8884d8"
                            ),
                            rx.recharts.bar(
                                data_key="neg", stroke="#82ca9d", fill="#82ca9d"
                            ),
                            rx.recharts.x_axis(data_key="name"),
                            rx.recharts.y_axis(),
                            rx.recharts.legend(),
                            data=data,
                        ),
                        # 새로 생성해야 함
                        # href="/analysis",
                    ),
                ),
                # rx.card(
                #     "graph",
                #     width="100%",
                #     height="100%",
                # ),
                width="50%",
            ),
            rx.spacer(),
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
