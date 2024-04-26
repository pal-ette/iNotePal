from sentence_transformers import SentenceTransformer
from .inference_model import InferenceModel


class EmbeddingModel(InferenceModel):

    def __init__(self, version) -> None:
        self.model = SentenceTransformer("jhgan/ko-sroberta-multitask")

    def tokenize(self, string):
        return string

    def padding(self, string):
        return string

    def predict(self, string):
        embedding = self.model.encode(string)
        return embedding
