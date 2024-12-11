import reflex as rx
from collections import Counter
from typing import List

from app.state.chat_state import ChatState

# ['공포' '기쁨' '놀람' '분노' '슬픔' '중립' '혐오']


class EmotionState(ChatState):
    def get_bg_color(self, emotion_count):

        if len(emotion_count) == 0:
            return "white"

        bg_color = f"linear-gradient(45deg, "
        ratio = 0
        base = sum(emotion_count.values())

        for i, (k, v) in enumerate(emotion_count.items()):
            bg_color = (
                bg_color
                + f"{self.emotion_color_map[k]} {ratio}% {ratio+round((emotion_count[k]/base)*100)}%, "
            )
            ratio += round((emotion_count[k] / base) * 100)

        return bg_color[:-2] + ")"

    @rx.var
    def get_bg_for_one(self) -> str:
        current_chats = self.current_messages

        emotions = [c.emotion.value for c in current_chats if c.is_user]

        emotion_count = Counter(emotions)
        return self.get_bg_color(emotion_count)

    @rx.var
    def get_bg(self) -> List[str]:
        past_chats = self.past_messages
        bg_colors = []

        emotions_of_the_day = [
            [id, [c.emotion.value for c in chats if c.is_user]]
            for (id, chats) in past_chats[::-1]
        ]

        if len(emotions_of_the_day) > 0:
            for _, emotions in emotions_of_the_day:
                emotion_count = Counter(emotions)
                bg_colors.append(self.get_bg_color(emotion_count))
        return bg_colors


def create_box():
    return rx.box(
        bg=EmotionState.get_bg_for_one,
        border_radius="10px",
        width="100%",
        height="10vh",
    )


def create_boxes(params):
    return rx.box(
        bg=params,
        border_radius="10px",
        width="8em",
    )


def emotion_card() -> rx.Component:

    return (
        rx.grid(
            rx.foreach(
                EmotionState.get_bg,
                create_boxes,
            ),
            spacing="2",
            width="100%",
            height="30vh",
            flex_wrap="wrap",
            grid_template_columns=[
                "repeat(3, 1fr)",
            ],
        ),
    )


def create_color_legend(color):

    return rx.hstack(
        rx.text("●", color=color[1], font_size="1em"),
        rx.text(color[0], font_size="1em"),
    )


def show_emotion_colors(emotion_color_map) -> rx.Component:

    return rx.hstack(rx.foreach(emotion_color_map, create_color_legend))
