from itertools import groupby

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = "keyt5-craft"

# Загрузка модели и токенизатора
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)


def process_text(s):
    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
    s = [el for el, _ in groupby(s)]
    return s


def generate(text, **kwargs):
    """Функция для генерации тэгов."""
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
    return process_text(tokenizer.decode(hypotheses[0], skip_special_tokens=True))


# Чтение текста из файла
with open("learning_data/text.txt", "r") as file:
    text = file.read()

tags = set(generate(text, top_p=1.0, max_length=64))

# Запись результата в файл
with open("learning_data/text_tags.txt", "w") as file:
        file.write(f"{text};{tags}")
