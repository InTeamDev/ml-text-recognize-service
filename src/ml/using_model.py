from itertools import groupby
from typing import List

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Название переобученной модели
MODEL_NAME = "keyt5-craft"

# Загрузка модели и токенизатора
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)


class TagsService:
    def __init__(self, text: str):
        self.text = text

    def generate_tags(self, text, top_p=1.0, max_length=64):
        inputs = tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            hypotheses = model.generate(**inputs, num_beams=5, top_p=1.0, max_length=64)
        s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
        s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
        s = set([el for el, _ in groupby(s)])
        return s
