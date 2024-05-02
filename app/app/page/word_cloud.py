import reflex as rx
from app.component.navbar import navbar
from app.component.word_cloud import word_cloud
from app.state.word_cloud_state import *
from app.page.login import require_login


@require_login
def wordcloud_page():

    return rx.flex(
        navbar(),
        rx.container(
            margin_top="120px",
        ),
        rx.hstack(
            rx.container(margin_left="100px"),
            rx.spacer(),
            rx.vstack(
                rx.hstack(
                    rx.chakra.heading(
                        WordCloudState.db_select_date,
                        size="xl",
                        weight="bold",
                        align="center",
                        padding_bottom="2vh",
                    ),
                    rx.spacer(),
                    rx.button(
                        "Show",
                        on_click=WordCloudState.update,
                        bg="#e5988e",
                    ),
                ),
                rx.spacer(),
                word_cloud(words=WordCloudState.display_words),
                width="100%",
            ),
            rx.spacer(),
            rx.container(margin_right="100px"),
            height="100%",
            # margin="10px",
        ),
        # rx.box(flex_grow=1),
        justify_content="start",
        width="100%",
        height="100%",
        # min_height="100vh",
        direction="column",
    )
