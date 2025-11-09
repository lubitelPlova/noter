from fastapi import FastAPI
from .routes import router
from contextlib import asynccontextmanager
from .database import async_session_maker, engine
from sqlalchemy import text
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Логирование для конкретных библиотек
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("🔧 Starting application...")

    # Тестируем подключение к БД
    try:
        print("🔍 Testing database connection...")
        async with async_session_maker() as session:
            # Простой запрос для проверки подключения
            result = await session.execute(text("SELECT version()"))
            db_version = result.scalar()
            print((
                f"✅ Database connection successful."
                f" PostgreSQL version: {db_version}"
            ))

            # Проверяем, что наши таблицы существуют
            result = await session.execute(
                text(("SELECT table_name FROM information_schema.tables WHERE "
                      "table_schema = 'public'"))
            )
            tables = result.scalars().all()
            print(f"📊 Found {len(tables)} tables in database: {tables}")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise

    print("🚀 Application startup complete!")

    yield  # Здесь приложение работает

    # Shutdown event
    print("🛑 Shutting down application...")
    await engine.dispose()
    print("✅ Application shutdown complete")

app = FastAPI(
    title="REST API microservie for creating notes",
    description="A simple microservice for note creatin",
    lifespan=lifespan
)

app.include_router(router)
