import reflex as rx
from reflex_calendar import calendar
from app.component.chat_input import chat_input
from app.component.chat_history import chat_history
from app.app_state import AppState
from app.state.chat_state import ChatState
from app.page.login import require_login


def navbar(sidebar: rx.Component = None) -> rx.Component:
    return rx.flex(
        # banner(),
        rx.flex(
            rx.link(
                rx.text(
                    "home",
                ),
                href="/",
            ),
            # navigation_section(),
            rx.box(
                flex_grow="1",
            ),
            rx.flex(
                # search_bar(),
                # github(),
                rx.box(
                    rx.card("B"),
                    display=["none", "none", "none", "none", "flex", "flex"],
                ),
                rx.box(
                    rx.chakra.popover(
                        rx.chakra.popover_trigger(rx.chakra.button(rx.icon("user"))),
                        rx.chakra.popover_content(
                            rx.chakra.popover_header("USER"),
                            rx.chakra.popover_body(
                                rx.chakra.button(
                                    "Logout",
                                    width="100%",
                                    on_click=[
                                        AppState.do_logout,
                                        AppState.check_login,
                                    ],
                                ),
                            ),
                            rx.chakra.popover_close_button(),
                        ),
                    ),
                    display=["flex", "flex", "flex", "flex", "none", "none"],
                ),
                spacing="3",
                align_items="center",
            ),
            background_color=rx.color("mauve", 1),
            border_bottom=f"1px solid {rx.color('mauve', 4)}",
            width="100%",
            align_items="center",
            spacing="5",
            padding="7px 20px 7px 20px;",
        ),
        width="100%",
        z_index="5",
        top="0px",
        position="fixed",
        align_items="center",
        direction="column",
    )


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
                        height="800px",
                        width="100%",
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
