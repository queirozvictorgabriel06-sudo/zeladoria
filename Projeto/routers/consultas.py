from fastapi import APIRouter
from tables.problema import read_problema
from tables.bairros import read_bairro


router = APIRouter(tags=["Consultas Básicas"])

@router.get("/bairros")
def listar_bairros():
    return read_bairro()


@router.get("/problemas")
def listar_problemas():
    return read_problema()

