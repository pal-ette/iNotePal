import reflex as rx
from collections import Counter
from typing import List, Tuple, Dict

from app.state.chat_state import ChatState
from app.util.emotion import emotion_color_map

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
                + f"{emotion_color_map[k]} {ratio}% {ratio+round((emotion_count[k]/base)*100)}%, "
            )
            ratio += round((emotion_count[k] / base) * 100)

        return bg_color[:-2] + ")"

    @rx.var
    def get_box_params_for_one(self) -> str:

        current_chats = self.current_messages
        box_params = []

        emotions = [c[2] for c in current_chats if c[0] == "user"]

        emotion_count = Counter(emotions)
        bg_colors = self.get_bg_color(emotion_count)

        return bg_colors

    @rx.var
    def get_box_params(self) -> List[Tuple[str, str, str]]:

        past_chats = self.past_messages
        box_params = []

        emotions_of_the_day = [
            [id, [c[2] for c in chats if c[0] == "user"]]
            for (id, chats) in past_chats[::-1]
        ]

        num_chat = len(emotions_of_the_day)

        height = str(int(100 / ((num_chat // 3) + 1))) + "%"
        width = (
            str(100 if num_chat == 1 else 32 if num_chat == 3 or num_chat > 4 else 49)
            + "%"
        )

        if len(emotions_of_the_day) > 0:
            for id, emotions in emotions_of_the_day:
                emotion_count = Counter(emotions)
                bg_colors = self.get_bg_color(emotion_count)

                box_params.append((id, bg_colors, width, height))
        return box_params


def create_box():

    return rx.box(
        bg=EmotionState.get_box_params_for_one,
        border_radius="10px",
        width="100%",
        height="10vh",
    )


def create_boxes(params):

    return rx.box(
        bg=params[1],
        border_radius="10px",
        width="8em",  # params[2],
        # height=params[3],
    )


def emotion_card() -> rx.Component:

    return (
        rx.flex(
            rx.foreach(EmotionState.get_box_params, create_boxes),
            spacing="2",
            width="100%",
            height="30vh",
            flex_wrap="wrap",
        ),
    )


def create_color_legend(color):

    return rx.hstack(
        rx.text("●", color=color[1], font_size="1em"),
        rx.text(color[0], font_size="1em"),
    )


def show_emotion_colors() -> rx.Component:

    return rx.hstack(rx.foreach(emotion_color_map, create_color_legend))
