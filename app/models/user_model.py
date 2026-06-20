from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(
        String, primary_key=True
    )

    nome = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    senha_hash = Column(
        String,
        nullable=False
    )

    tarefas = relationship(
        "Tarefa",
        back_populates="usuario"
    )

    criado_em = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

