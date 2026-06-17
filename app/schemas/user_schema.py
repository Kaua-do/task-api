from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):

    nome: str = Field(
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    senha: str = Field(
        min_length=6,
        max_length=100,
    )


class UserLogin(BaseModel):

    email: EmailStr

    senha: str = Field(
        min_length=1
    )


class UserResponse(BaseModel):

    id: str
    nome: str
    email: str

    model_config = ConfigDict(
        from_attributes=True
    )

class UserUpdate(BaseModel):

    nome: str = Field(
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    senha_atual: str = Field(
        min_length=1
    )


class ChangePassword(BaseModel):

    senha_atual: str = Field(
        min_length=1
    )

    nova_senha: str = Field(
        min_length=6,
        max_length=100,
    )


