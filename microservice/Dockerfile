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

# Создаем non-root пользователя
# RUN groupadd -r fastapi && useradd -r -g fastapi fastapi

# # Копируем приложение
COPY  microservice/app/ ./app/

# # Переключаемся на non-root пользователя
# USER fastapi

# Health check
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD curl -f http://127.0.0.1:8000/health || exit 1

EXPOSE 8000

COPY microservice/alembic.ini .
COPY microservice/startup.sh .

RUN chmod +x startup.sh
# Используем shell форму для переменных окружения
# CMD ["fastapi", "run" ]
ENTRYPOINT ["./startup.sh"]