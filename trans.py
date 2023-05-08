import whisper, json

model = whisper.load_model("base")

result = model.transcribe("audio.mp3", fp16 = False)
text = result['text']

with open('sentences_starts.json', 'w', encoding='utf-8') as f:
    json.dump(text, f, ensure_ascii=False, indent=4)
    f.close()


