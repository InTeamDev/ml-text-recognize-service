import random
import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from transformers import T5ForConditionalGeneration, T5Tokenizer
from tqdm import trange

# Гиперпараметры
RAW_MODEL = '0x7194633/keyt5-large'
BATCH_SIZE = 4
REPORT_STEPS = 200
EPOCHS = 3
LEARNING_RATE = 1e-5
NEW_MODEL_NAME = 'keyT5-custom'

# Загрузка модели и токенизатора
def load_model_and_tokenizer(raw_model):
    model = T5ForConditionalGeneration.from_pretrained(raw_model).cuda()
    tokenizer = T5Tokenizer.from_pretrained(raw_model)
    return model, tokenizer

# Генерация пар батчей
def batch_pairs(pairs, batch_size):
    random.shuffle(pairs)
    return [pairs[i * batch_size: (i + 1) * batch_size] for i in range(int(len(pairs) / batch_size))]

# Тестирование модели
def test_model(model, tokenizer, df, sample_size=5):
    sample = df.sample(sample_size)
    for i, row in sample.iterrows():
        print(row.X)
        print('real:', row.Y)
        print('model: ', answer(row.X, model, tokenizer))
        print('---')

# Ответ модели
def answer(x, model, tokenizer, **kwargs):
    inputs = tokenizer(x, return_tensors='pt').to(model.device)
    with torch.no_grad():
        hypotheses = model.generate(**inputs, **kwargs)
    return tokenizer.decode(hypotheses[0], skip_special_tokens=True)

# Загрузка данных
df = pd.read_csv('dataset/train.csv')
pd.options.display.max_colwidth = 500
df_train, df_test = train_test_split(df.dropna(), test_size=0.5, random_state=1)
pairs = df_train[['X', 'Y']].values.tolist()

# Загрузка модели и токенизатора
model, tokenizer = load_model_and_tokenizer(RAW_MODEL)

# Оптимизатор
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Обучение модели
model.train()
losses = []
for epoch in range(EPOCHS):
    print('EPOCH', epoch)
    for i, batch in enumerate(trange(0, batch_pairs(pairs, BATCH_SIZE))):
        x = tokenizer([p[0] for p in batch], return_tensors='pt', padding=True).to(model.device)
        y = tokenizer([p[1] for p in batch], return_tensors='pt', padding=True).to(model.device)
        y.input_ids[y.input_ids == 0] = -100
        loss = model(input_ids=x.input_ids, attention_mask=x.attention_mask, labels=y.input_ids, decoder_attention_mask=y.attention_mask, return_dict=True).loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        losses.append(loss.item())
        if i % REPORT_STEPS == 0:
            print('step', i, 'loss', np.mean(losses[-REPORT_STEPS:]))

# Перевод модели в режим оценки
model.eval()

# Тестирование модели на тренировочных и тестовых данных
test_model(model, tokenizer, df_train)
test_model(model, tokenizer, df_test)

# Сохранение модели и токенизатора
model.save_pretrained(NEW_MODEL_NAME)
tokenizer.save_pretrained(NEW_MODEL_NAME)
