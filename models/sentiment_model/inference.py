import os, pickle, torch
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import OrderedDict

device = torch.device("cuda:0")

def load_dict(file_path, model):

    best_model = torch.load(file_path)

    label = best_model['label']
    pretrained_dict = best_model['state_dict']
    renamed_pretrained_dict = OrderedDict([(k.replace('roberta.', ''), v) for k, v in pretrained_dict.items()])

    model_dict = model.state_dict()

    model_dict.update(renamed_pretrained_dict)
    model.load_state_dict(model_dict)

    return model, label

def inference(sentence, model):

  attention_mask = sentence['attention_mask'].to(device)
  input_ids = sentence['input_ids'].squeeze(1).to(device)

  out = model(input_ids, attention_mask)[0]
  max_vals, max_indices = torch.max(out, 1)

  return max_indices

if __name__ == '__main__':

    MODEL_NAME = 'klue/roberta-large'
    roberta_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=7)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # change file_path
    file_path = 'roberta-large_7-emotions.pt'
    roberta_model = roberta_model.to(device)
    model, label = load_dict(file_path, roberta_model)

    text = ''

    x = tokenizer(text, truncation=True, padding='max_length', max_length=64, return_tensors='pt')
    p_idx = inference(x, model)
    prediction = label[p_idx] # predicted emotion in Korean