from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class MediaItem(Base):
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, index=True)  #ID из TMDB
    title = Column(String, index=True)
    overview = Column(Text, nullable=True)
    poster_path = Column(String, nullable=True)
    media_type = Column(String)     #'movie' или 'tv'
    release_date = Column(String, nullable=True)    #для фильмов; для сериалов - first_air_date
    genres = Column(JSON, nullable=True)    #список жанров
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="planned")      # planned, watching, completed, dropped
    rating = Column(Integer, nullable=True)     # от 1 до 10
    