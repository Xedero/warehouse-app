from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, items

# Создаём таблицы при старте (если база доступна)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warehouse App")

# Подключаем роутеры
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])

# Главная страница
@app.get("/")
def root():
    return {"message": "Warehouse App is running"}

# Health check для Render (HEAD /)
@app.head("/")
def head_root():
    return {"status": "ok"}
