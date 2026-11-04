from fastapi import APIRouter, HTTPException
from schemas.categoria import CategoriaSchema
from tables.categoria_problema import (
    create_categoria_problema, 
    read_categoria_problema,
    delete_categoria_problema
)


router = APIRouter(prefix="/categorias", tags=["Categorias (Administrador)"])

@router.get("/")
def listar_categorias():
    return read_categoria_problema()


@router.post("/", status_code=201)
def registrar_categoria(dados: CategoriaSchema):
    resultado = create_categoria_problema(
        id_problema=dados.id_problema,
        gravidade=dados.gravidade
    )
    if not resultado:
        raise HTTPException(status_code=400, detail="Erro ao registar. Verifique o ID do problema.")
    return {"mensagem": "Categoria registada com sucesso!", "dados": resultado}


@router.delete("/{id_categoria}")
def apagar_categoria(id_categoria: int):
    resultado = delete_categoria_problema(id_categoria)
    if not resultado:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return {"mensagem": "Categoria apagada!", "dados": resultado}