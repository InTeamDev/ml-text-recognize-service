from itertools import groupby
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = "keyt5-craft"

# Загрузка модели и токенизатора
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# Предобработки сгенерированного текста
def process_text(s):
    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
    s = [el for el, _ in groupby(s)]
    return s

# Функция для генерации текста с помощью модели
def generate(text, **kwargs):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
    return process_text(tokenizer.decode(hypotheses[0], skip_special_tokens=True))


# Чтение текста из файла
with open("text.txt", "r") as file:
    article = file.read()

tags = generate(article, top_p=1.0, max_length=64)

# Запись результата в файл
with open("output.txt", "w") as file:
        file.write(f"{article};{tags}")
