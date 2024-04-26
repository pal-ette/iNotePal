import reflex as rx
from app.component.word_cloud import word_cloud
from app.state.word_cloud_state import WordCloudState


def wordcloud_page() -> rx.Component:
    return rx.vstack(
        word_cloud(words=WordCloudState.display_words),
        rx.button(
            "추가",
            on_click=WordCloudState.add_text,
        ),
        align="center",
    )
