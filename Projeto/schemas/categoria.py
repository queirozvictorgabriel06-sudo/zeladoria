from pydantic import BaseModel, Field

from pydantic import BaseModel, field_validator

class CategoriaSchema(BaseModel):
    id_problema: int
    gravidade: int


    @field_validator('gravidade')
    @classmethod
    def validar_gravidade_bonita(cls, valor_digitado):
        if valor_digitado not in [1, 2, 3]:
            raise ValueError("Oops! A gravidade é inválida. Use apenas 1 (Baixo), 2 (Médio) ou 3 (Grave).")
        return valor_digitado