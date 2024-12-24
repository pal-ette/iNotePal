import reflex as rx
from reflex.style import toggle_color_mode

from app.app_state import AppState
from app.state.chat_state import ChatState
from app.component.emotion_card import emotion_card, show_emotion_colors
from app.state.calendar_state import calendar_component
from app.routes import DASHBOARD_ROUTE, ANALYSIS_ROUTE
from app.component.color_picker import color_picker


def navbar() -> rx.Component:
    return rx.fragment(
        rx.flex(
            rx.flex(
                rx.link(
                    rx.heading(
                        "iNP",
                        size="6",
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
                        size="6",
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
                    href=DASHBOARD_ROUTE,
                    color="initial",
                    text_decoration="none",
                ),
                rx.hstack(
                    rx.link(
                        rx.text(
                            "Analysis",
                            color_scheme="gray",
                        ),
                        href=ANALYSIS_ROUTE,
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
                                        ChatState.do_logout,
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
                    rx.dialog.root(
                        rx.dialog.trigger(rx.button(rx.icon("settings"))),
                        rx.dialog.content(
                            rx.dialog.title(
                                rx.hstack(
                                    rx.heading("설정"),
                                    rx.dialog.close(
                                        rx.button(
                                            rx.icon("circle-x"),
                                            variant="ghost",
                                        ),
                                    ),
                                    justify="between",
                                ),
                            ),
                            rx.heading(
                                "색상 설정",
                                size="3",
                            ),
                            rx.hstack(
                                rx.foreach(
                                    ChatState.emotion_color_map,
                                    lambda emotion_color: rx.vstack(
                                        rx.hstack(
                                            rx.text(emotion_color[0]),
                                            rx.cond(
                                                emotion_color[1]
                                                == ChatState.emotion_color_map_default[
                                                    emotion_color[0]
                                                ],
                                                rx.fragment(),
                                                rx.button(
                                                    rx.icon(
                                                        "undo-2",
                                                        size=14,
                                                    ),
                                                    variant="ghost",
                                                    size="1",
                                                    on_click=ChatState.on_change_color(
                                                        emotion_color[0],
                                                        ChatState.emotion_color_map_default[
                                                            emotion_color[0]
                                                        ],
                                                    ),
                                                ),
                                            ),
                                            align="center",
                                        ),
                                        rx.popover.root(
                                            rx.popover.trigger(
                                                rx.box(
                                                    bg=emotion_color[1],
                                                    border_radius="10px",
                                                    width="4em",
                                                    height="4em",
                                                ),
                                            ),
                                            rx.popover.content(
                                                rx.vstack(
                                                    rx.text_field(
                                                        value=emotion_color[1],
                                                        color_scheme=emotion_color[1],
                                                        on_change=lambda value: ChatState.on_change_color(
                                                            emotion_color[0],
                                                            value,
                                                        ).debounce(
                                                            200
                                                        ),
                                                    ),
                                                    color_picker(
                                                        color=emotion_color[1],
                                                        on_change=lambda color: ChatState.on_change_color(
                                                            emotion_color[0],
                                                            color,
                                                        ).debounce(
                                                            200
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            modal=True,
                                        ),
                                        align="center",
                                    ),
                                ),
                            ),
                            on_pointer_down_outside=rx.prevent_default,
                        ),
                        is_centered=True,
                        modal=True,
                        on_open_change=ChatState.on_open_change_settings,
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
                                        size="6",
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
                                                href=ANALYSIS_ROUTE,
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
                                        select_date=ChatState.select_date,
                                        accent_dates=ChatState.dates_has_closed_chat,
                                        on_change_date=ChatState.on_change_date,
                                    ),
                                    rx.spacer(),
                                    rx.text(
                                        f"{ChatState.print_date_text}의 감정",
                                        # on_change=State.select_date,
                                        as_="i",
                                        font_size="1.5em",
                                        weight="bold",
                                    ),
                                    show_emotion_colors(ChatState.emotion_color_map),
                                    emotion_card(),
                                    # align_items="center",
                                ),  # drawer content end
                                top="auto",
                                right="auto",
                                height="100%",
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
