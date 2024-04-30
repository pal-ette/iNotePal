from sentence_transformers import SentenceTransformer
from .inference_model import InferenceModel
import torch
import multiprocessing as mp


def cuda_worker(input, output):
    device = torch.device("cuda:0")

    model = SentenceTransformer("jhgan/ko-sroberta-multitask")

    for _func, sentence in iter(input.get, "STOP"):
        output.put(model.encode(sentence))


class EmbeddingModel(InferenceModel):

    def __init__(self, version) -> None:
        ctx = mp.get_context("spawn")
        self.input_queue = ctx.Queue()
        self.output_queue = ctx.Queue()

        ctx.Process(
            target=cuda_worker,
            args=(
                self.input_queue,
                self.output_queue,
            ),
        ).start()

    def __del__(self):
        self.input_queue.put("STOP")

    def tokenize(self, string):
        return string

    def padding(self, string):
        return string

    def predict(self, string):
        self.input_queue.put((0, string))
        return self.output_queue.get()
