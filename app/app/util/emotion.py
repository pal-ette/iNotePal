import random


def emotions():
    return [
        "분노",
        "기쁨",
        "슬픔",
        "불안",
        "상처",
        "당황",
        "중립",
    ]


def random_emotion():
    return random.sample(emotions(), 1)[0]
