# how to use

### Recognize

Для транскрибации аудиопотока в текст, в файле `recognize.py` нужно использовать функцию `get`.

```python
import recognize

result = recognize.get("audio.mp3")
```

### Tags

Для получения ключевых слов в тексте, в файле `tags.py` нужно использовать функцию `get`.

```python
import tags

result = tags.get("Получение ключевых слов (тэгов) из текста")
```
