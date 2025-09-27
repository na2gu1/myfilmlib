from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import MediaItem
from app.schemas import MediaItemOut, MediaItemUpdate, MediaItemQueryParams
from app.tmdb import fetch_movie_details
from sqlalchemy import select, func

router = APIRouter(prefix="/media", tags=["Media"])

@router.post("/add-by-tmdb/{tmdb_id}", response_model=MediaItemOut)
async def add_media_by_tmbd_id(tmdb_id: int, db: AsyncSession = Depends(get_db)):
    # Проверяем, есть ли уже в БД
    result = await db.execute(select(MediaItem).where(MediaItem.tmdb_id == tmdb_id))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Movie already in your library")
    
    # Получаем из TMDB
    try:
        tmdb_data = await fetch_movie_details(tmdb_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TMDB API error: {str(e)}")
    
    # Сохраняем в БД
    db_item = MediaItem(tmdb_id=tmdb_id, **tmdb_data)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[MediaItemOut])
async def list_media_items(
    params: MediaItemQueryParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    query = select(MediaItem)

    # Поиск по названию (регистронезависимый)
    if params.search:
        query = query.where(MediaItem.title.ilike(f"%{params.search}%"))

    # Фильтрация по статусу
    if params.status:
        query = query.where(MediaItem.status == params.status)

    # Фильтрация по типу
    if params.media_type:
        query = query.where(MediaItem.media_type == params.media_type)

    # Пагинация
    query = query.offset(params.skip).limit(params.limit)

    result = await db.execute(query)
    items = result.scalars().all()
    return items

@router.patch("/{item_id}", response_model=MediaItemOut)
async def update_media_item(
    item_id: int,
    updates: MediaItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    # находим фильм
    result = await db.execute(select(MediaItem).where(MediaItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
    
    # обновляем только передние поля 
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item

@router.get("/stats")
async def get_media_stats(db: AsyncSession = Depends(get_db)):
    # Общее количество
    total = await db.scalar(select(func.count(MediaItem.id)))

    # Количество по статусам
    status_counts = await db.execute(
        select(MediaItem.status, func.count(MediaItem.id))
        .group_by(MediaItem.status)
    )
    by_status = {row[0]: row[1] for row in status_counts}

    # Средний рейтинг (игнорируем NULL)
    avg_rating = await db.scalar(select(func.avg(MediaItem.rating)))

    return {
        "total": total,
        "by_status": by_status,
        "average_rating": round(float(avg_rating), 2) if avg_rating else None
    }