from sqlalchemy.orm import Session

from app.models.categoria_model import Categoria


def criar_categorias_padrao(db: Session):

    categoria_existente = db.query(Categoria).first()

    if categoria_existente:
        return

    nomes_categorias = [
        "Academia",
        "Estudo",
        "Trabalho",
        "Casa",
        "Igreja",
        "Projeto",
        "Saúde",
        "Outros"
    ]

    categorias = [
        Categoria(nome=nome)
        for nome in nomes_categorias
    ]

    db.add_all(categorias)

    db.commit()


def listar_categorias_service(db: Session):

    categorias = db.query(Categoria).all()

    return categorias

