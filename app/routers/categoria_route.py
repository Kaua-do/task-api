from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.categoria_schema import CategoriaResponse
from app.services.categoria_service import listar_categorias_service
from app.dependencies.auth_dependency import (get_current_user)
from app.models.user_model import(Usuario)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
)

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)):
    return listar_categorias_service(db)


