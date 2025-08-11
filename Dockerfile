FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PYTHONUNBUFFERED=1


CMD ["gunicorn", "mis.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]