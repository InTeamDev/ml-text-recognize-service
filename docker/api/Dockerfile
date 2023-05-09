FROM python:3.9

WORKDIR /opt/service

RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq-dev ffmpeg \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD uvicorn main:app --reload --app-dir=src --host=0.0.0.0 --port=8000 --proxy-headers