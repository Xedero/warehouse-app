from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, items

# Создаём таблицы при старте (если DB доступна)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warehouse App")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
def root():
    return {"message": "Warehouse App is running"}
