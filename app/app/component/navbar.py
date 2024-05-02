import reflex as rx
from app.app_state import AppState
from app.state.chat_state import ChatState
from reflex_calendar import calendar
from app.component.emotion_card import emotion_card, show_emotion_colors

from app.page.calendar import calendar_grid, calendar_grid_row, calendar_days
from app.state.calendar_state import State


def navbar() -> rx.Component:
    return rx.fragment(
        rx.chakra.flex(
            # banner(),
            rx.flex(
                rx.chakra.heading(
                    "iNotePal",
                    as_="h1",
                    size="4xl",
                    weight="bold",
                    bgGradient="linear(to-l, #f2ebc8, #de776c, #49312d)",
                    bgClip="text",
                ),
                rx.link(
                    rx.text(
                        "Home",
                        color_scheme="gray",
                    ),
                    href="/",
                ),
                rx.link(
                    rx.text(
                        "Analysis",
                        color_scheme="gray",
                    ),
                    href="/analysis",
                ),
                rx.link(
                    rx.text(
                        "Word Cloud",
                        color_scheme="gray",
                    ),
                    href="/word_cloud",
                ),
                # navigation_section(),
                rx.box(
                    flex_grow="1",
                ),
                rx.flex(
                    # search_bar(),
                    # github(),
                    rx.flex(
                        rx.chakra.popover(
                            rx.chakra.popover_trigger(
                                rx.chakra.button(rx.icon("user"))
                            ),
                            rx.chakra.popover_content(
                                rx.chakra.popover_header(AppState.user_mail),
                                rx.chakra.popover_body(
                                    rx.chakra.button(
                                        "Logout",
                                        width="100%",
                                        on_click=[
                                            AppState.do_logout,
                                            AppState.check_login,
                                        ],
                                        variant="outline",
                                    ),
                                ),
                                rx.chakra.popover_close_button(),
                            ),
                        ),
                    ),
                    rx.drawer.root(
                        rx.drawer.trigger(rx.chakra.button(rx.icon("align-justify"))),
                        rx.drawer.overlay(z_index="5"),
                        rx.drawer.portal(
                            rx.drawer.content(
                                rx.vstack(
                                    rx.chakra.heading(
                                        "iNotePal",
                                        as_="h1",
                                        size="4xl",
                                        weight="bold",
                                        bgGradient="linear(to-l, #f2ebc8, #de776c, #49312d)",
                                        bgClip="text",
                                    ),
                                    rx.chakra.divider(border_color="black"),
                                    rx.spacer(),
                                    rx.chakra.text(
                                        "Calendar",
                                        as_="i",
                                        font_size="2em",
                                        weight="bold",
                                    ),
                                    calendar(
                                        locale="ko-KR",
                                        width="100%",
                                        on_change=ChatState.switch_day,
                                        value=ChatState.select_date,
                                    ),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon(
                                                tag="chevron_left",
                                                cursor="pointer",
                                                on_click=State.delta_calendar(-1),
                                            ),
                                            rx.spacer(),  # 빈 공간 생성
                                            rx.text(  # 현재 월과 연도를 표시하는 텍스트
                                                f"{State.month_class[State.month]} {State.year}",
                                                width="150px",
                                                display="flex",
                                                justify_content="center",
                                            ),
                                            rx.spacer(),
                                            rx.icon(
                                                tag="chevron_right",
                                                cursor="pointer",
                                                on_click=State.delta_calendar(1),
                                            ),
                                            display="flex",
                                            align_items="center",
                                            justify_content="center",
                                            spacing="2",
                                        ),
                                        rx.hstack(
                                            rx.foreach(
                                                State.date_class, calendar_days
                                            )  # Example
                                        ),
                                        rx.foreach(
                                            State.calendar_data, calendar_grid
                                        ),  # Example
                                    ),
                                    rx.spacer(),
                                    rx.chakra.text(
                                        State.selected_date,
                                        # on_change=State.select_date,
                                        as_="i",
                                        font_size="2em",
                                        weight="bold",
                                    ),
                                    show_emotion_colors(),
                                    emotion_card(),
                                ),
                                top="auto",
                                right="auto",
                                height="100%",
                                width="40%",
                                padding="1em",
                                background_color="#FFF",
                            )
                        ),
                        direction="left",
                        spacing="1",
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
            align_items="left",
            direction="column",
        ),
    )
