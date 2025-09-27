from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text  
from app.database import get_db
from app.config import settings
from dotenv import load_dotenv
from app.routers import media

load_dotenv()

app = FastAPI(
    title="MyFilmLib API",
    description="Сервис для управления личной библиотекой фильмов и сериалов",
    version="0.1.0"
)

app.include_router(media.router)

@app.get("/")
async def root():
    return {"message": "Welcome to MyFilmLib! 🎬"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Используем text() для сырого SQL
        result = await db.execute(text("SELECT 1"))
        db_status = "connected" if result.scalar() == 1 else "error"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "OK",
        "database": db_status,
        "environment": settings.DATABASE_URL.split(":")[0]
    }