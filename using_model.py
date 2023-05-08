from itertools import groupby
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = "0x7194633/keyt5-large"

# Загрузка модели и токенизатора
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def process_text(s):
    """Функция для предобработки сгенерированного текста."""
    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
    s = [el for el, _ in groupby(s)]
    return s

def generate(text, **kwargs):
    """Функция для генерации текста с помощью модели."""
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
    return process_text(tokenizer.decode(hypotheses[0], skip_special_tokens=True))


article = """Жизнь человека неразрывно связана с родной природой, с землей. Земля - это наша кормилица..."""

print(generate(article, top_p=1.0, max_length=64))
