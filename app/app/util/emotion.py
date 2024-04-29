import random


def emotions():
    return [
        "공포",
        "기쁨",
        "놀람",
        "분노",
        "슬픔",
        "중립",
        "혐오",
    ]


def random_emotion():
    return random.sample(emotions(), 1)[0]
