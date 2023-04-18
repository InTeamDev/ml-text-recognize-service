import math

import numpy as np
from scipy.signal import argrelextrema
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# загрузка текста из файла
with open("test.txt") as f:
    doc = f.readlines()
    print("Text:")
    print(doc[0])
    f.close()
doc = doc[0].replace("?", ".").replace("!", ".")
sentences = doc.split('. ')

# загрузка модели предобученных векторных представлений предложений
model = SentenceTransformer('all-mpnet-base-v2')

# получение векторных представлений предложений
embeddings = model.encode(sentences)

# создание матрицы косинусных сходств
similarities = cosine_similarity(embeddings)


# применение функции активации к матрице сходств
def rev_sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(0.5 * x))


def activate_similarities(similarities: np.array, p_size=10) -> np.array:
    if p_size > similarities.shape[0]:
        p_size = similarities.shape[0]

    x = np.linspace(-10, 10, p_size)
    y = np.vectorize(rev_sigmoid)
    activation_weights = np.pad(y(x), (0, similarities.shape[0] - p_size))
    diagonals = [similarities.diagonal(each) for each in range(0, similarities.shape[0])]
    diagonals = [np.pad(each, (0, similarities.shape[0] - len(each))) for each in diagonals]
    diagonals = np.stack(diagonals)
    diagonals = diagonals * activation_weights.reshape(-1, 1)
    activated_similarities = np.sum(diagonals, axis=0)
    return activated_similarities


activated_similarities = activate_similarities(similarities, p_size=10)
minmimas = argrelextrema(activated_similarities, np.less, order=2)

# разбиение текста на абзацы
split_points = [each for each in minmimas[0]]
print("\nResult:")
text = ''
for num, each in enumerate(sentences):
    if num in split_points:
        text += f'\n\n {each}. '
    else:
        text += f'{each}. '

print(text)
