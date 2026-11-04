from fastapi import APIRouter, HTTPException
from schemas.ocorrencias import OcorrenciaSchema 
from tables.ocorrencias import create_ocorrencias, read_ocorrencias, delete_ocorrencias

router = APIRouter(prefix="/ocorrencias", tags=["Ocorrências"])

@router.get("/")
def listar_ocorrencias():
    return read_ocorrencias()


@router.post("/", status_code=201)
def registrar_ocorrencia(dados: OcorrenciaSchema):
    resultado = create_ocorrencias(
        id_categoria=dados.id_categoria_p,
        id_bairro=dados.id_bairros
    )
    if not resultado:
        raise HTTPException(
            status_code=400, 
            detail="Erro ao registar. Verifique se os IDs existem."
        )
    return {"mensagem": "Ocorrência registada com sucesso!", "dados": resultado}


@router.delete("/{id_ocorrencia}")
def deletar_ocorrencia(id_ocorrencia: int):
    resultado = delete_ocorrencias(id_ocorrencia)

    if resultado is None:
        raise HTTPException(status_code=404, detail="Ocorrência não encontrada.")
    if resultado is False:
        raise HTTPException(status_code=500, detail="Erro ao deletar a ocorrência.")

    return {"mensagem": "Ocorrência deletada com sucesso!", "dados": resultado}