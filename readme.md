# ml service

API для транскрибации аудиолекций

**Авторы**:

`Backend+DevOps+Infra` - Павел (ZetoOfficial) <br>
`ML` - Александр (Chelozzi) <br>

## Документация

### ReDoc

http://localhost:8000/api/redoc

### Docs

https://localhost:8000/api/docs

## Запуск (using docker)

### Requirements

1. Install mkcert - https://github.com/FiloSottile/mkcert
2. Docker and Docker-compose - https://linuxhint.com/install-docker-compose-windows/
3. Make (optional) - https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows

### Запуск после установки того, что выше:

#### Установка сертификатов

```bash
mkcert -install
mkcert localhost

# перемещаем сертификаты в папку certs
mkdir certs
move localhost.pem certs/
move localhost-key.pem certs/
```

#### Запуск

```bash
# если установлен make, то
make up

# если нет, тогда
docker-compose -f docker/docker-compose.dev.yml up --build -d

# глянуть логи
make logs
# или
docker-compose -f docker/docker-compose.dev.yml logs -f --tail 100 api
```

## Запуск (native)

### Requirements

1. Install Python3.9 (ВАЖНО ИМЕННО 3.9)
2. Install ffmpeg - https://phoenixnap.com/kb/ffmpeg-windows
3. Install mkcert - https://github.com/FiloSottile/mkcert

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
pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
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
.venv\Scripts\activate.bat

# install requirements
pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
pip install -r requirements.txt
pip install -e src/

# copy config file + заполняем его
copy src\core\.env.example src\core\.env
# Нужно обязательно указать mongo_dsn!!!

# run service
uvicorn main:app --app-dir=src --host=localhost --port=8000 --proxy-headers --ssl-keyfile=.\certs\localhost-key.pem --ssl-certfile=.\certs\localhost.pem
```
