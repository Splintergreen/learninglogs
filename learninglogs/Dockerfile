FROM python:3.10-slim

# Установка необходимых пакетов для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    g++ \
    make \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./ /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "learninglogs.wsgi:application", "--bind", "0.0.0.0:8000" ]
