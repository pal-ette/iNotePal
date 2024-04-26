import reflex as rx
from collections import Counter
from typing import List

from app.component.chat_input import chat_input
from app.component.chat_history import chat_history
from app.component.navbar import navbar
from app.state.chat_state import ChatState
from app.page.login import require_login

# ['공포' '기쁨' '놀람' '분노' '슬픔' '중립' '혐오']


class EmotionState(rx.State):

    chat_data: List[dict[int, dict[str, int]]] = [
        {2: {"분노": 1, "슬픔": 1}},
        {2: {"혐오": 1, "분노": 1}},
    ]

    def emotion_cnt(self):
        data = []
        for i, (key, value) in enumerate(self.chat_data.items()):
            emotions = [v["emotion"] for v in value]
            emotion_count = Counter(emotions)
            data.append([len(self.chat_data), emotion_count])

        return data


# def get_box_params(emotion_cnt):


def create_box(params):

    # param is presented as a list key-value pair([2, dict], [2, dict])

    num_chat = params[0]
    emotion_cnt = params[1]

    colors = {
        "혐오": "#49312d",
        "분노": "#91615a",
        "공포": "#af625c",
        "슬픔": "#de776c",
        "중립": "#e5988e",
        "놀람": "#ebb9b0",
        "기쁨": "#f2ebc8",
    }

    bg_colors = f"linear-gradient(45deg, "
    ratio = 0
    base = sum(emotion_cnt.values())

    for k in emotion_cnt:
        bg_colors = (
            bg_colors
            + f"{colors[k]} {ratio}% {ratio+round((emotion_cnt[k]/base)*100)}%, "
        )
        ratio += round((emotion_cnt[k] / base) * 100)

    bg_colors = bg_colors[:-7] + ")"

    height = int(100 / ((num_chat // 3) + 1))
    width = 100 if num_chat == 1 else 33 if num_chat == 3 or num_chat > 4 else 50

    return rx.box(
        background=bg_colors,
        border_radius="10px",
        width=f"{width}%",
        height=f"{height}%",
    )


def emotion_card() -> rx.Component:

    dummy = {
        "chat1": (
            {
                "is_user": True,
                "message": "안녕5",
                "emotion": "분노",
                "created_at": "2022-02-22 10:12:12.000",
            },
            {
                "is_user": True,
                "message": "안녕6",
                "emotion": "슬픔",
                "created_at": "2022-02-22 10:12:42.000",
            },
        ),
        "chat2": (
            {
                "is_user": True,
                "message": "안녕7",
                "emotion": "혐오",
                "created_at": "2022-02-22 10:13:12.000",
            },
            {
                "is_user": True,
                "message": "안녕8",
                "emotion": "분노",
                "created_at": "2022-02-22 10:13:30.000",
            },
        ),
    }

    return rx.flex(
        rx.foreach(EmotionState.test, create_box),
        spacing="2",
        width="100%",
        height="20vh",
    )
