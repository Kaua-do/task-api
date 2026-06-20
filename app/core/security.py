from datetime import datetime, timedelta, UTC
from jose import jwt
from passlib.context import CryptContext
from jose import JWTError
from fastapi import HTTPException
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_access_token(
        data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.now(UTC)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def hash_senha(
        senha: str
):

    return pwd_context.hash(
        senha
    )

def verificar_senha(
        senha: str,
        senha_hash: str
):

    return pwd_context.verify(
        senha,
        senha_hash
    )


def verificar_token(
        token: str
):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return user_id

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

