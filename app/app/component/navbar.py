import reflex as rx
from reflex.style import toggle_color_mode

from app.app_state import AppState
from app.state.chat_state import ChatState
from app.component.emotion_card import emotion_card, show_emotion_colors
from app.state.calendar_state import calendar_component
from app.routes import DASHBOARD_ROUTE, ANALYSIS_ROUTE
from app.component.color_picker import color_picker
from app.component.logo import logo


def navbar() -> rx.Component:
    return rx.fragment(
        rx.flex(
            rx.flex(
                rx.link(
                    logo(
                        "iNP",
                        display=[
                            "flex",
                            "flex",
                            "none",
                            "none",
                            "none",
                            "none",
                        ],
                    ),
                    logo(
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
                            "통계",
                            color_scheme=rx.cond(
                                rx.State.router.page.path == ANALYSIS_ROUTE,
                                "#de776c",
                                "gray",
                            ),
                            class_name=f"hover:text-[#de776c] {rx.cond(rx.State.router.page.path == ANALYSIS_ROUTE, 'border-b-2 border-b-[#de776c]', '')}  py-3",
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
                    rx.dialog.root(
                        rx.dialog.trigger(rx.button(rx.icon("settings"))),
                        rx.dialog.content(
                            rx.vstack(
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
                                    class_name="w-full",
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
                                                            rx.text(
                                                                "#",
                                                                size="5",
                                                                padding="0px 0px 0px 10px",
                                                            ),
                                                            value=emotion_color[1][1:],
                                                            color_scheme=emotion_color[
                                                                1
                                                            ],
                                                            on_change=lambda value: ChatState.on_change_color(
                                                                emotion_color[0],
                                                                f"#{value}",
                                                            ).debounce(
                                                                200
                                                            ),
                                                            class_name="flex-row-reverse items-center",
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
                                rx.divider(),
                                rx.heading(
                                    "대화 설정",
                                    size="3",
                                ),
                                rx.checkbox(
                                    "대화에 OpenAI 를 사용",
                                    checked=ChatState.use_openai_chatting,
                                    on_change=ChatState.on_change_use_openai_chatting,
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
                                    rx.hstack(
                                        logo(),
                                        rx.drawer.close(
                                            rx.button(
                                                rx.icon("circle-x"),
                                                variant="ghost",
                                            ),
                                        ),
                                        class_name="justify-between items-center w-full",
                                    ),
                                    rx.divider(border_color="black"),
                                    rx.hstack(
                                        rx.spacer(),
                                        rx.text(
                                            AppState.authenticated_user.username,
                                        ),
                                        rx.button(
                                            "로그아웃",
                                            on_click=[
                                                ChatState.do_logout,
                                            ],
                                            variant="outline",
                                        ),
                                        width="100%",
                                        align_items="center",
                                    ),
                                    rx.spacer(),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.link(
                                                rx.text(
                                                    "통계",
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
                                        allow_future=False,
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
                                background_color="var(--color-background)",
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
                padding="0px 20px 0px 20px",
            ),
            width="100%",
            z_index="5",
            top="0px",
            position="fixed",
            align_items="left",
            direction="column",
        ),
    )
