import httpx
from app.config import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"

async def fetch_movie_details(tmdb_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}",
            params={"api_key": settings.TMDB_API_KEY}
        )
        if response.status_code == 404:
            raise ValueError("Movie not found in TMDB")
        response.raise_for_status()  # выбросит исключение при 4xx/5xx
        data = response.json()
        return {
            "title": data["title"],
            "overview": data.get("overview"),
            "poster_path": f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else None,
            "release_date": data.get("release_date"),
            "genres": [g["name"] for g in data.get("genres", [])],
            "media_type": "movie"
        }