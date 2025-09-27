from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

class MediaItemBase(BaseModel):
    tmdb_id: int
    title: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    media_type: str     # 'movie' or 'tv'
    release_date: Optional[str] = None
    genres: Optional[List[str]] = None
    status: Optional[str] = 'planned'
    rating: Optional[int] = None

class MediaItemCreate(MediaItemBase):
    pass

class MediaItemOut(MediaItemBase):
    id: int
    added_at: datetime

    model_config = {"from_attributes": True}

class MediaItemUpdate(BaseModel):
    status: Optional[str] = None
    rating: Optional[int] = None

    @field_validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('Rating must be between 1 and 10')
        return v
    
class MediaItemQueryParams(BaseModel):
    search: Optional[str] = None
    status: Optional[str] = None
    media_type: Optional[str] = None
    skip: int = 0
    limit: int = 10

    # валидация limit максимум 100 за раз
    @field_validator('limit')
    def validate_limits(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Limit must be between 1 and 100')
        return v
    