import reflex as rx
from konlpy.tag import Kkma
from collections import Counter
from typing import List, Dict
from app.state.chat_state import ChatState


class WordCloudState(ChatState):

    display_words: List[Dict[str, str | int]] = []
    including = ["NNG", "NNM", "NNP", "NP", "UN", "VA", "VV", "MA"]

    @rx.var
    def words_from_current_chat(self):

        kkma = Kkma()

        current_chat = self.current_messages
        messages = [c[1] for c in current_chat if c[0] == "user"]

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
        print("words : ", words)

        return words

    def add_text(self):
        words = self.words_from_current_chat
        if len(self.display_words) == len(self.words_from_current_chat):
            return
        self.display_words.append(words[len(self.display_words)])
