from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import verificar_token
from app.models.user_model import Usuario

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
        token: str = Depends(
            oauth2_scheme
        ),
        db: Session = Depends(
            get_db
        )
):

    user_id = verificar_token(token)

    usuario = (db.query(Usuario).filter(Usuario.id == user_id).first())

    return usuario

