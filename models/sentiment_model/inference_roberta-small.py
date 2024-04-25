import os, pickle, torch, re
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import OrderedDict
from torch.autograd import Variable

device = torch.device("cuda:0")

class RobertaClassifier(nn.Module):
    def __init__(self, base_model, num_classes, dr_rate, hidden_size):
        super().__init__()

        self.dr_rate = dr_rate
        self.roberta = base_model.roberta
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.roberta_classifier = base_model.classifier
        self.dense = nn.Linear(hidden_size, 384)
        # self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dr_rate)
        self.classifier = nn.Linear(384 , num_classes)
        # self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):

        h_0 = Variable(torch.zeros(1, len(input_ids), hidden_size).cuda())
        c_0 = Variable(torch.zeros(1, len(input_ids), hidden_size).cuda())

        out = self.roberta(input_ids=input_ids, attention_mask=attention_mask)[0]
        out, (h, c) = self.lstm(out, (h_0, c_0))
        out = self.roberta_classifier(out)
        out = self.dense(out)
        # out = self.relu(out)
        out = self.dropout(out)
        out = self.classifier(out)
        # out = self.softmax(out)

        return out

def load_dict(file_path, model):

    best_model = torch.load(file_path)

    label = best_model['label']
    pretrained_dict = best_model['state_dict']

    model_dict = model.state_dict()

    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)

    return model.to(device), label

def inference(sentence, model):

    attention_mask = sentence['attention_mask'].to(device)
    input_ids = sentence['input_ids'].squeeze(1).to(device)

    out = model(input_ids, attention_mask)
    max_vals, max_indices = torch.max(out, 1)

    return max_indices

if __name__ == '__main__':

    MODEL_NAME = 'klue/roberta-small'
    hidden_size = 768
    roberta_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=hidden_size)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # change file_path
    file_path = 'roberta-small_7-emotions.pt'
    roberta_model = roberta_model
    model = RobertaClassifier(roberta_model, 7, 0.2, 768)
    model, label = load_dict(file_path, model)

    text = ''
    text = re.sub(r"[^가-힣ㅏ-ㅣㄱ-ㅎA-Za-z0-9,!?]", " ", text)

    x = tokenizer(text, truncation=True, padding='max_length', max_length=64, return_tensors='pt')
    p_idx = inference(x, model)
    prediction = label[p_idx] # predicted emotion in Korean