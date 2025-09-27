from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # логирует SQL-запросы в консоль — полезно при разработке
    future=True  # включает режим SQLAlchemy 2.0
)

# Создаем фабрику сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False  # не закрывать объекты после коммита
)

# Dependency для FastAPI — будет внедряться в эндпоинты
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session