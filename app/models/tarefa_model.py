from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Tarefa(Base):

    __tablename__ = "tarefas"

    id = Column(String, primary_key=True)

    titulo = Column(String)

    descricao = Column(String)

    prioridade = Column(String, nullable=True)

    status = Column(String)

    criado_em = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    data_prazo = Column(
        Date,
        nullable=True,
    )

    data_conclusao = Column(
        DateTime(timezone=True),
        nullable=True
    )

    usuario_id = Column(
        String, ForeignKey("usuarios.id")
    )

    usuario = relationship("Usuario", back_populates="tarefas")

    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=True)

    categoria = relationship("Categoria", back_populates="tarefas")





