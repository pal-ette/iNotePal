import reflex as rx


class DialogState(rx.State):

    emotion_card_opened: bool = False
    conv_opened: bool = False

    def emotion_opens(self, value: bool):
        self.emotion_card_opened = value

    def conv_opens(self, value: bool):
        self.conv_opened = value
