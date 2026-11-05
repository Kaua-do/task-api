from fastapi import FastAPI

from app.database import engine, Base

from app.models.user_model import Usuario
from app.models.tarefa_model import Tarefa
from app.models.categoria_model import Categoria

from app.routers.tarefa_route import router as tarefa_router
from app.routers import user_route
from app.routers.auth_route import router as auth_router
from app.routers.categoria_route import router as categoria_router
from app.database import SessionLocal
from app.services.categoria_service import (criar_categorias_padrao)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "mensagem": "API funcionando!"
    }

app.include_router(tarefa_router)

app.include_router(auth_router)

app.include_router(user_route.router)

app.include_router(categoria_router)




