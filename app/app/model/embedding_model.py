from sentence_transformers import SentenceTransformer
from .inference_model import InferenceModel
import faiss
import pandas as pd


class EmbeddingModel(InferenceModel):
    def __init__(self, version) -> None:
        super().__init__(version)

        self.model = SentenceTransformer("jhgan/ko-sroberta-multitask")

        self.paths = {
            "index": f"https://github.com/pal-ette/iNotePal/releases/download/{version}/embedding_index.index",
            "data": f"https://github.com/pal-ette/iNotePal/releases/download/{version}/embedding_data.csv",
        }

        self.index = faiss.read_index(self.download_file(self.paths["index"]))

        self.df = pd.read_csv(self.download_file(self.paths["data"]))

    def tokenize(self, string):
        return string

    def padding(self, string):
        return string

    def predict(self, string):
        response = None
        embedding = self.model.encode(string)
        _distances, indices = self.index.search(embedding.reshape(1, -1), 5)
        return self.df.iloc[indices[0][0]]["answer"]
