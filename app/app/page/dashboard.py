import reflex as rx
from reflex_calendar import calendar
from app.component.chat_input import chat_input
from app.component.chat_history import chat_history, ai_chat_bubble
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


def build_past_card(chat):
    return rx.button(
        chat["id"],
        on_click=lambda: ChatState.select_past_card(chat["id"]),
    )


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
                    ChatState.has_past_chats,
                    rx.scroll_area(
                        rx.hstack(
                            rx.foreach(
                                ChatState.past_chats,
                                build_past_card,
                            ),
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
                        rx.vstack(
                            chat_history(),
                            chat_input(ChatState.is_exist_chat),
                            rx.cond(
                                ChatState.is_closed,
                                rx.hstack(
                                    rx.badge(
                                        ChatState.chat_emotion,
                                    ),
                                    rx.button(
                                        "대화 새로 시작하기",
                                        on_click=ChatState.start_new_chat,
                                    ),
                                ),
                                rx.button(
                                    "대화 마치기",
                                    on_click=ChatState.evaluate_chat,
                                    width="100%",
                                    variant="soft",
                                    size="4",
                                ),
                            ),
                            align="center",
                            width="100%",
                        ),
                    ),
                    width="100%",
                    # height="800px",
                ),
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
