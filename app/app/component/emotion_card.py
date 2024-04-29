import reflex as rx
from datetime import datetime
from collections import Counter
from typing import List, Tuple, Dict

from app.component.chat_input import chat_input
from app.component.chat_history import chat_history
from app.component.navbar import navbar
from app.state.chat_state import ChatState
from app.page.login import require_login

# ['공포' '기쁨' '놀람' '분노' '슬픔' '중립' '혐오']


class EmotionState(ChatState):

    colors = {
        "혐오": "#49312d",
        "분노": "#91615a",
        "공포": "#af625c",
        "슬픔": "#de776c",
        "중립": "#e5988e",
        "당황": "#ebb9b0",
        "기쁨": "#f2ebc8",
    }

    @rx.var  # return을 foreach 변수로 부를 수 있음!
    def get_box_params(self) -> List[Tuple[str, str, str]]:

        past_chats = self.past_messages
        box_params = []

        emotions_of_the_day = [
            [c[2] for c in chats if c[0] == "user"] for chats in past_chats
        ]

        num_chat = len(emotions_of_the_day)

        height = str(int(100 / ((num_chat // 3) + 1))) + "%"
        width = (
            str(100 if num_chat == 1 else 33 if num_chat == 3 or num_chat > 4 else 50)
            + "%"
        )

        if len(emotions_of_the_day) > 0:
            for emotions in emotions_of_the_day:
                emotion_count = Counter(emotions)

                bg_colors = f"linear-gradient(45deg, "
                ratio = 0
                base = sum(emotion_count.values())

                for i, (k, v) in enumerate(emotion_count.items()):
                    bg_colors = (
                        bg_colors
                        + f"{self.colors[k]} {ratio}% {ratio+round((emotion_count[k]/base)*100)}%, "
                    )
                    ratio += round((emotion_count[k] / base) * 100)

                # print("bg_colors", bg_colors)
                bg_colors = bg_colors[:-6] + ")"

                box_params.append((bg_colors, width, height))

        print(box_params)

        return box_params


def create_box(params):

    return rx.box(
        background=params[0],
        border_radius="10px",
        width=params[1],
        height=params[2],
    )


def emotion_card() -> rx.Component:

    return rx.flex(
        rx.foreach(EmotionState.get_box_params, create_box),
        spacing="2",
        width="100%",
        height="20vh",
    )
