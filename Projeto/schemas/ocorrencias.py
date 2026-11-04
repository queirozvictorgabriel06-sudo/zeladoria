from pydantic import BaseModel

class OcorrenciaSchema(BaseModel):
    id_categoria_p : int
    id_bairros : int