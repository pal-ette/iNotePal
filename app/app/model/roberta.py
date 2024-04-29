import os, pickle, torch, re
from torch import nn
from torch.autograd import Variable
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import OrderedDict
from .inference_model import InferenceModel
import multiprocessing as mp
import time


class RobertaClassifier(nn.Module):
    def __init__(self, base_model, num_classes, dr_rate, hidden_size):
        super().__init__()

        self.hidden_size = hidden_size
        self.roberta = base_model.roberta
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.roberta_classifier = base_model.classifier
        self.dense = nn.Linear(hidden_size, 384)
        # self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dr_rate)
        self.classifier = nn.Linear(384, num_classes)
        # self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):

        h_0 = Variable(torch.zeros(1, len(input_ids), self.hidden_size).cuda())
        c_0 = Variable(torch.zeros(1, len(input_ids), self.hidden_size).cuda())

        out = self.roberta(input_ids=input_ids, attention_mask=attention_mask)[0]
        out, (h, c) = self.lstm(out, (h_0, c_0))
        out = self.roberta_classifier(out)
        out = self.dense(out)
        # out = self.relu(out)
        out = self.dropout(out)
        out = self.classifier(out)
        # out = self.softmax(out)

        return out


def cuda_worker(model_name, model_path, input, output):
    def load_dict(file_path, model):

        best_model = torch.load(file_path)

        label = best_model["label"]
        pretrained_dict = best_model["state_dict"]
        # renamed_pretrained_dict = OrderedDict(
        #     [(k.replace("roberta.", ""), v) for k, v in pretrained_dict.items()]
        # )

        model_dict = model.state_dict()

        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)

        return model, label

    device = torch.device("cuda:0")

    roberta_model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=768,
    )

    roberta_model = RobertaClassifier(roberta_model, 7, 0.2, 768)

    roberta_model = roberta_model.to(device)

    model, label = load_dict(model_path, roberta_model)

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    for _func, sentence in iter(input.get, "STOP"):
        sentence = re.sub(r"[^가-힣ㅏ-ㅣㄱ-ㅎA-Za-z0-9,!?]", " ", sentence)

        sentence = tokenizer(
            sentence,
            truncation=True,
            padding="max_length",
            max_length=64,
            return_tensors="pt",
        )

        attention_mask = sentence["attention_mask"].to(device)
        input_ids = sentence["input_ids"].squeeze(1).to(device)

        out = model(input_ids, attention_mask)  # [0]
        max_vals, max_indices = torch.max(out, 1)

        prediction = label[max_indices]  # predicted emotion in Korean
        output.put(prediction)


class Roberta(InferenceModel):

    def __init__(self, version) -> None:
        super().__init__(version)

        self.model_name = "klue/roberta-small"

        self.path = f"https://github.com/pal-ette/iNotePal/releases/download/{version}/roberta-small_7-emotions.pt"
        self.model_path = self.download_file(self.path)

        self.input_queue = mp.Queue()
        self.output_queue = mp.Queue()

        cuda_process = mp.Process(
            target=cuda_worker,
            args=(
                self.model_name,
                self.model_path,
                self.input_queue,
                self.output_queue,
            ),
        )
        cuda_process.start()

    def tokenize(self, string):
        return string

    def padding(self, tokenzied_string):
        return tokenzied_string

    def predict(self, sentence):
        self.input_queue.put((0, sentence))
        return self.output_queue.get()
