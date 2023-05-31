FROM python:3.9

WORKDIR /opt/ml_service

RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq-dev ffmpeg \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir
RUN pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz

COPY . .

RUN pip install -e src

RUN python src/download_model.py

CMD uvicorn main:app --app-dir=src --host=0.0.0.0 --port=8000 --proxy-headers --ssl-keyfile=./certs/localhost-key.pem --ssl-certfile=./certs/localhost.pem