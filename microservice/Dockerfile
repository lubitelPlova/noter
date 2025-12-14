FROM python:3.8-slim AS builder

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY microservice/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.8-slim

WORKDIR /app

# Копируем зависимости из builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Устанавливаем только runtime зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Копируем приложение
COPY  microservice/app/ ./app/


EXPOSE 8000

COPY microservice/alembic.ini .
COPY microservice/startup.sh .

RUN chmod +x startup.sh

ENTRYPOINT ["./startup.sh"]