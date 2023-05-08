import whisper

model = whisper.load_model("base")

result = model.transcribe("audio.mp3", fp16 = False)
text = result['text']

with open('text.txt', 'w', encoding='utf-8') as f:
    f.write(text)



