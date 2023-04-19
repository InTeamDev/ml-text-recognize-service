import whisper, json

model = whisper.load_model("base")

result = model.transcribe("audio.mp3", fp16 = False)

sentences = [segment['text'] for segment in result['segments']]
starts = [segment['start'] for segment in result['segments']]
sentences_starts = dict(zip(sentences, starts))

with open('sentences_starts.json', 'w', encoding='utf-8') as f:
    json.dump(sentences_starts, f, ensure_ascii=False, indent=4)
    f.close()


