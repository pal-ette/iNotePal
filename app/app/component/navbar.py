import reflex as rx
import reflex_chakra as rc
from app.app_state import AppState
from app.state.chat_state import ChatState
from reflex_calendar import calendar
from app.component.emotion_card import emotion_card, show_emotion_colors

from app.state.calendar_state import calendar_component


def date_to_print(date):
    return date.split("-")


def navbar() -> rx.Component:
    return rx.fragment(
        rc.flex(
            rx.flex(
                rx.link(
                    rc.heading(
                        "iNP",
                        as_="h1",
                        size="4xl",
                        weight="bold",
                        bgGradient="linear(to-l, #f2ebc8, #de776c, #49312d)",
                        bgClip="text",
                        display=[
                            "flex",
                            "flex",
                            "none",
                            "none",
                            "none",
                            "none",
                        ],
                    ),
                    rc.heading(
                        "iNotePal",
                        as_="h1",
                        size="4xl",
                        weight="bold",
                        bgGradient="linear(to-l, #f2ebc8, #de776c, #49312d)",
                        bgClip="text",
                        display=[
                            "none",
                            "none",
                            "flex",
                            "flex",
                            "flex",
                            "flex",
                        ],
                    ),
                    href="/",
                ),
                rc.hstack(
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
                    display=[
                        "none",
                        "none",
                        "flex",
                        "flex",
                        "flex",
                        "flex",
                    ],
                ),
                rx.box(
                    flex_grow="1",
                ),
                rx.flex(
                    # search_bar(),
                    # github(),
                    rx.flex(
                        rc.popover(
                            rc.popover_trigger(rc.button(rx.icon("user"))),
                            rc.popover_content(
                                rc.popover_header(AppState.user_mail),
                                rc.popover_body(
                                    rc.button(
                                        "Logout",
                                        width="100%",
                                        on_click=[
                                            AppState.do_logout,
                                            AppState.check_login,
                                        ],
                                        variant="outline",
                                    ),
                                ),
                                rc.popover_close_button(),
                            ),
                        ),
                    ),
                    rx.drawer.root(
                        rx.drawer.trigger(rc.button(rx.icon("align-justify"))),
                        rx.drawer.overlay(z_index="5"),
                        rx.drawer.portal(
                            rx.drawer.content(
                                rx.vstack(
                                    rc.heading(
                                        "iNotePal",
                                        as_="h1",
                                        size="4xl",
                                        weight="bold",
                                        bgGradient="linear(to-l, #f2ebc8, #de776c, #49312d)",
                                        bgClip="text",
                                    ),
                                    rc.divider(border_color="black"),
                                    rx.spacer(),
                                    rc.vstack(
                                        rc.hstack(
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
                                        ),
                                        rc.divider(border_color="black"),
                                        rx.spacer(),
                                        width="100%",
                                        display=[
                                            "flex",
                                            "flex",
                                            "none",
                                            "none",
                                            "none",
                                            "none",
                                        ],
                                    ),
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
                                    rx.spacer(),
                                    rc.text(
                                        f"{ChatState.print_date_text}의 감정",
                                        # on_change=State.select_date,
                                        as_="i",
                                        font_size="1.5em",
                                        weight="bold",
                                    ),
                                    show_emotion_colors(),
                                    emotion_card(),
                                    # align_items="center",
                                ),  # drawer content end
                                top="auto",
                                right="auto",
                                height="100%",
                                width="27em",
                                padding="1em",
                                background_color="#FFF",
                            )
                        ),
                        direction="left",
                        spacing="1",
                    ),  # drawer root end
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
