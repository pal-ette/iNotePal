import random


emotion_color_map_default = {
    "혐오": "#49312d",
    "분노": "#91615a",
    "공포": "#af625c",
    "슬픔": "#de776c",
    "중립": "#e5988e",
    "놀람": "#ebb9b0",
    "기쁨": "#f2ebc8",
}


def random_emotion():
    return random.sample(sorted(emotion_color_map_default), 1)[0]
