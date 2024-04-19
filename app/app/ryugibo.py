from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from .inference_model import InferenceModel


class Ryugibo(InferenceModel):

    def __init__(self, version) -> None:
        super().__init__(version)

        self.paths = {
            "model": f"https://github.com/pal-ette/iNotePal/releases/download/{version}/ryugibo_model.keras",
            "tokenizer": f"https://github.com/pal-ette/iNotePal/releases/download/{version}/ryugibo_tokenizer.pickle",
            "y_label_binarizer": f"https://github.com/pal-ette/iNotePal/releases/download/{version}/ryugibo_label_binarizer.pickle",
            "config": f"https://github.com/pal-ette/iNotePal/releases/download/{version}/ryugibo_config.pickle",
        }
        self.model = load_model(self.download_file(self.paths["model"]))
        self.tokenizer = self.load_pickle_file(
            self.download_file(self.paths["tokenizer"])
        )
        self.y_label_binarizer = self.load_pickle_file(
            self.download_file(self.paths["y_label_binarizer"])
        )
        self.seq_length = self.load_pickle_file(
            self.download_file(self.paths["config"])
        )["seq_length"]

    def tokenize(self, string):
        return self.tokenizer.texts_to_sequences(string)

    def padding(self, tokenzied_string):
        return pad_sequences(
            tokenzied_string,
            maxlen=self.seq_length,
        )

    def predict(self, padded_tokenized_string):
        return self.y_label_binarizer.inverse_transform(
            self.model.predict(padded_tokenized_string)
        )
