# ml service

API для транскрибации аудиолекций

**Авторы**:

`Backend+DevOps+Infra` - Павел (ZetoOfficial) <br>
`ML` - Александр (Chelozzi) <br>

## Документация

### ReDoc

http://0.0.0.0:8000/api/redoc

### Docs

http://0.0.0.0:8000/api/docs

## Запуск

1. Install ffmpeg - https://ffmpeg.org/download.html
2. Install mkcert - https://github.com/FiloSottile/mkcert
   2.2 Настроить сертификаты:

### Linux/MacOS

**Install mkcert**

```bash
mkcert -install
mkcert localhost

# перемещаем сертификаты в папку certs
mkdir certs
mv localhost.pem certs/
mv localhost-key.pem certs/
```

**Setup environment**

```bash
# set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install requirements
pip install -r requirements.txt
pip install -e src/

# copy config file + заполняем его
cp src/core/.env.example src/core/.env

# run service
uvicorn main:app --app-dir=src --host=localhost --port=8000 --proxy-headers --ssl-keyfile=./certs/localhost-key.pem --ssl-certfile=./certs/localhost.pem
```

### Windows

**Install mkcert**

```bash
mkcert -install
mkcert localhost

# перемещаем сертификаты в папку certs
mkdir certs
move localhost.pem certs/
move localhost-key.pem certs/
```

**Setup environment**

```bash
# set up virtual environment
python -m venv .venv
venv\Scripts\activate.bat

# install requirements
venv pip install -r requirements.txt
pip install -e src/

# copy config file + заполняем его
copy src/core/.env.example src/core/.env

# run service
uvicorn main:app --app-dir=src --host=localhost --port=8000 --proxy-headers --ssl-keyfile=./certs/localhost-key.pem --ssl-certfile=./certs/localhost.pem
```
