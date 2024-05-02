import reflex as rx
from app.component.navbar import navbar
from app.component.word_cloud import word_cloud
from app.state.word_cloud_state import WordCloudState


def wordcloud_page() -> rx.Component:
    return rx.flex(
        navbar(),
        rx.container(
            margin_top="120px",
        ),
        rx.vstack(
            word_cloud(words=WordCloudState.display_words),
            rx.button(
                "추가",
                on_click=WordCloudState.add_text,
            ),
            align="center",
        ),
    )
