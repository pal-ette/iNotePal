import reflex as rx
import reflex_chakra as rc
from reflex_wordcloud import wordcloud
from app.component.navbar import navbar
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
                    rc.heading(
                        WordCloudState.print_date_text,
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
                wordcloud(
                    words=WordCloudState.display_words,
                    options={
                        "colors": [
                            "#49312d",
                            "#91615a",
                            "#af625c",
                            "#de776c",
                            "#e5988e",
                            "#ebb9b0",
                            "#f2ebc8",
                        ],
                        "rotations": 2,
                        "rotationAngles": [-90, 0],
                        "fontFamily": "impact",
                        "padding": 1,
                        "scale": "sqrt",
                        "fontSizes": [10, 60],
                        "fontStyle": "normal",
                    },
                ),
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
