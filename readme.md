# ml service

API для транскрибации аудиолекций

Backend+DevOps+Infra - Павел (ZetoOfficial)
ML - Александр (Chelozzi)

## Запуск

### (docker + make)

```bash
make up
```

### Native

(linux/macos)

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# mongo connect data
export DB_HOST="mongodb"
export DB_PORT=27017
export DB_DATABASE="ml"

uvicorn main:app --reload --app-dir=src --host=0.0.0.0 --port=8000 --proxy-headers
```

## Документация

### ReDoc

http://0.0.0.0:8000/api/redoc

### Docs

http://0.0.0.0:8000/api/docs
