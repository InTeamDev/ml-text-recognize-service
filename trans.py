import whisper
import librosa
import pandas as pd
import numpy as np

# Загрузка модели Whisper
model = whisper.load_model("base")

# Загрузка аудио-файла
audio = whisper.load_audio("C://kjk//audio.mp3")
audio = whisper.pad_or_trim(audio)

# Вычисление спектрограммы мел
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# Транскрибация аудио-файла
options = whisper.DecodingOptions(fp16 = False)
result = whisper.decode(model, mel, options)
text = result.text

# Разделение текста на предложения
sentences = []
current_sentence = ''
for i in range(len(text)):
    if text[i].isupper() and i > 0 and text[i-1] == ' ':
        sentences.append(current_sentence.strip())
        current_sentence = text[i]
    else:
        current_sentence += text[i]
sentences.append(current_sentence.strip())
print(sentences)


# Определение временных меток для каждого предложения
filename = "C://kjk//audio.mp3"
audio, sr = librosa.load(filename, sr=None)
audio = whisper.pad_or_trim(audio)
timestamps = []
for sentence in sentences:
    start = result.text.index(sentence)
    duration = librosa.get_duration(y=audio, sr=sr)
    end = start + len(sentence)
    end_time = librosa.frames_to_time(end * 5, sr=sr)
    start_time = librosa.frames_to_time(start * 5, sr=sr)
    timestamps.append((start_time, end_time))

# Сохранение временных меток в таблицу
df = pd.DataFrame(timestamps, columns=["start_time", "end_time"])
df["sentence"] = sentences
#df.to_csv("C://kjk//timestamps.csv", index=False)

# Вывод результата
print(df)
