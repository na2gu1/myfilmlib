## Запуск локально

1. Создай `.env` на основе `.env.example`
2. Установи зависимости: `pip install -r requirements.txt`
3. Запусти: `uvicorn app.main:app --reload`

## Деплой

Задеплоить на [Render](https://render.com/) или [Railway](https://railway.app/):
- Укажи команду запуска: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Добавь переменные окружения из `.env`