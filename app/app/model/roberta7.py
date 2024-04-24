import os, pickle, torch
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import OrderedDict
from .inference_model import InferenceModel


class Roberta(InferenceModel):

    def __init__(self, version) -> None:
        super().__init__(version)

        self.device = torch.device("cuda:0")

        self.model_name = "klue/roberta-large"

        self.path = f"https://github.com/pal-ette/iNotePal/releases/download/{version}/roberta-large_7-emotions.pt"
        self.model_path = self.download_file(self.path)

        roberta_model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=7,
        )

        roberta_model = roberta_model.to(self.device)

        self.model, self.label = self.load_dict(self.model_path, roberta_model)

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self.y_label_binarizer = self.load_pickle_file(
            self.download_file(self.paths["y_label_binarizer"])
        )
        self.seq_length = self.load_pickle_file(
            self.download_file(self.paths["config"])
        )["seq_length"]

    def tokenize(self, string):
        return self.tokenizer(
            string,
            truncation=True,
            padding="max_length",
            max_length=64,
            return_tensors="pt",
        )

    def padding(self, tokenzied_string):
        return tokenzied_string

    def predict(self, sentence):
        attention_mask = sentence["attention_mask"].to(self.device)
        input_ids = sentence["input_ids"].squeeze(1).to(self.device)

        out = self.model(input_ids, attention_mask)[0]
        max_vals, max_indices = torch.max(out, 1)

        prediction = self.label[max_indices]  # predicted emotion in Korean
        return prediction

    def load_dict(self, file_path, model):

        best_model = torch.load(file_path)

        label = best_model["label"]
        pretrained_dict = best_model["state_dict"]
        renamed_pretrained_dict = OrderedDict(
            [(k.replace("roberta.", ""), v) for k, v in pretrained_dict.items()]
        )

        model_dict = model.state_dict()

        model_dict.update(renamed_pretrained_dict)
        model.load_state_dict(model_dict)

        return model, label
