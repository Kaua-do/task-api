from sqlalchemy import Column, String, Integer
from app.database import Base
from sqlalchemy.orm import relationship

class Categoria(Base):

    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)

    nome = Column(String, unique=True, nullable=False)

    tarefas = relationship(
        "Tarefa",
        back_populates="categoria"
    )
