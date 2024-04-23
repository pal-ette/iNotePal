import reflex as rx
from app.app_state import AppState


def navbar() -> rx.Component:
    return rx.fragment(
        rx.chakra.flex(
            # banner(),
            rx.flex(
                rx.chakra.heading(
                    "Pal-ette",
                    as_="h1",
                    size="4xl",
                    weight="bold",
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
                        "History",
                        color_scheme="gray",
                    ),
                    href="/",
                ),
                rx.link(
                    rx.text(
                        "Analysis",
                        color_scheme="gray",
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
                        display=["flex", "flex", "flex", "flex", "flex", "flex"],
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
