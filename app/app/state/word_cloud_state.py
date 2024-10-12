import reflex as rx
from konlpy.tag import Kkma
from collections import Counter
from datetime import datetime
from typing import List, Dict, Tuple
from app.state.chat_state import ChatState


class WordCloudState(ChatState):

    display_words: List[Dict[str, str | int]] = []
    including = ["NNG", "NNM", "NNP", "NP"]  # , "VA", "VV", "MA"]

    @rx.var
    def words_from_past_chat(self):

        kkma = Kkma()

        past_chats = self.past_messages
        messages = [c[1] for (id, chats) in past_chats for c in chats if c[0] == "user"]

        if messages == []:
            return messages

        messages = " ".join(messages)
        morphs = []
        pos = kkma.pos(messages)
        for w in pos:
            if w[1] in self.including:
                morphs.append(w[0])

        words_count = Counter(morphs)
        words = [
            {"text": key, "value": value}
            for i, (key, value) in enumerate(words_count.items())
        ]

        return words

    def update(self):
        self.display_words = self.words_from_past_chat
