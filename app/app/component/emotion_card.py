import reflex as rx
from collections import Counter
from typing import List, Tuple, Dict

from app.state.chat_state import ChatState
from app.state.dialog_state import DialogState
from app.component.word_cloud import WordCloud
from app.page.word_cloud import wordcloud_page

# ['공포' '기쁨' '놀람' '분노' '슬픔' '중립' '혐오']


class EmotionState(ChatState):

    colors = {
        "혐오": "#49312d",
        "분노": "#91615a",
        "공포": "#af625c",
        "슬픔": "#de776c",
        "중립": "#e5988e",
        "놀람": "#ebb9b0",
        "기쁨": "#f2ebc8",
    }

    # @rx.var
    # def emotion_ratio(self, chat_id) -> Dict:
    #     chats = self.get_messages(chat_id)
    #     emotions = [c[2] for c in chats if c[0] == "user"]
    #     emotion_count = Counter(emotions)

    #     base = sum(emotion_count.values())

    #     for i, (k, v) in enumerate(emotion_count.items()):
    #         emotion_count[k] = f"{round((emotion_count[k] / base) * 100)}%"

    #     print("emotion count : ", emotion_count)

    #     return emotion_count

    def get_bg_color(self, emotion_count):

        if len(emotion_count) == 0:
            return "white"

        bg_color = f"linear-gradient(45deg, "
        ratio = 0
        base = sum(emotion_count.values())

        for i, (k, v) in enumerate(emotion_count.items()):
            bg_color = (
                bg_color
                + f"{self.colors[k]} {ratio}% {ratio+round((emotion_count[k]/base)*100)}%, "
            )
            ratio += round((emotion_count[k] / base) * 100)

        # print("bg_colors", bg_colors)
        return bg_color[:-2] + ")"

    @rx.var  # return을 foreach 변수로 부를 수 있음!
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

    # @rx.var
    # def emotion_modal():
    #     bg = EmotionState.get_box_params[-1][1]
    #     return rx.chakra.box(bg=bg, border_radius="md", width="50%", height="50%")


def create_boxes(params):

    # dialog
    return rx.flex(
        rx.dialog.root(
            rx.dialog.trigger(
                rx.chakra.box(
                    rx.center(
                        rx.chakra.button(
                            params[0],
                            variant="unstyled",
                            size="sm",
                            # on_click=DialogState.change,
                        ),
                    ),
                    bg=params[1],
                    width="10vh",
                    height="10vh",
                    border_radius="10px",
                    # padding=5,
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("오늘의 감정"),
                rx.dialog.description("Description"),
                rx.flex(
                    rx.hstack(
                        rx.text("Emotion Ratio"),
                        rx.spacer(),
                        rx.text("Word Cloud"),
                        # emotion_dialog(params[0]), rx.spacer(), rx.text("Word Cloud")
                    )
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button("닫기", size="1"),
                    ),
                    justify="end",
                ),
            ),
            on_open_change=DialogState.emotion_opens,
        ),
    )

    # simple boxes
    # return rx.chakra.box(
    #     bg=params[1],
    #     border_radius="10px",
    #     width=params[2],
    #     height=params[3],
    # )


# def show_ratio(params):

#     return rx.chakra.text(params)
#     # return rx.hstack(
#     #     rx.chakra.text(params[0], font_size="1em"),
#     #     rx.chakra.text(params[1], font_size="1em"),
#     # )


# def emotion_dialog(chat_id) -> rx.Component:

#     return rx.chakra.card(
#         rx.chakra.vstack(rx.foreach(EmotionState.emotion_ratio(chat_id), show_ratio))
#     )


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
        rx.chakra.text("●", color=color[1], font_size="1em"),
        rx.chakra.text(color[0], font_size="1em"),
    )


def show_emotion_colors() -> rx.Component:

    return rx.hstack(rx.foreach(EmotionState.colors, create_color_legend))
