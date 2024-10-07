import reflex as rx
from reflex.style import toggle_color_mode

from app.app_state import AppState
from app.state.chat_state import ChatState
from app.component.emotion_card import emotion_card, show_emotion_colors
from app.state.calendar_state import calendar_component


def date_to_print(date):
    return date.split("-")


def navbar() -> rx.Component:
    return rx.fragment(
        rx.flex(
            rx.flex(
                rx.link(
                    rx.heading(
                        "iNP",
                        size="4xl",
                        weight="bold",
                        background="linear-gradient(to left, #f2ebc8, #de776c, #49312d)",
                        background_clip="text",
                        color="transparent",
                        display=[
                            "flex",
                            "flex",
                            "none",
                            "none",
                            "none",
                            "none",
                        ],
                    ),
                    rx.heading(
                        "iNotePal",
                        size="4xl",
                        weight="bold",
                        background="linear-gradient(to left, #f2ebc8, #de776c, #49312d)",
                        background_clip="text",
                        color="transparent",
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
                    color="initial",
                    text_decoration="none",
                ),
                rx.hstack(
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
                    rx.button(
                        rx.color_mode_cond(
                            light=rx.icon("moon"),
                            dark=rx.icon("sun"),
                        ),
                        on_click=toggle_color_mode,
                    ),
                    rx.flex(
                        rx.popover.root(
                            rx.popover.trigger(rx.button(rx.icon("user"))),
                            rx.popover.content(
                                rx.text(AppState.user_mail),
                                rx.button(
                                    "Logout",
                                    width="100%",
                                    on_click=[
                                        AppState.do_logout,
                                        AppState.check_login,
                                    ],
                                    variant="outline",
                                ),
                                rx.popover.close(
                                    rx.button("Close"),
                                    width="100%",
                                ),
                            ),
                        ),
                    ),
                    rx.drawer.root(
                        rx.drawer.trigger(rx.button(rx.icon("align-justify"))),
                        rx.drawer.overlay(z_index="5"),
                        rx.drawer.portal(
                            rx.drawer.content(
                                rx.vstack(
                                    rx.heading(
                                        "iNotePal",
                                        as_="h1",
                                        size="4xl",
                                        weight="bold",
                                        background="linear-gradient(to left, #f2ebc8, #de776c, #49312d)",
                                        background_clip="text",
                                        color="transparent",
                                    ),
                                    rx.divider(border_color="black"),
                                    rx.spacer(),
                                    rx.vstack(
                                        rx.hstack(
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
                                        rx.divider(border_color="black"),
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
                                    rx.text(
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
                                background_color=rx.color_mode_cond(
                                    light="white",
                                    dark="black",
                                ),
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
