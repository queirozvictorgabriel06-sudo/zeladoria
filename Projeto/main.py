from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import consultas, ocorrencias, categorias
from pathlib import Path
from fastapi.responses import FileResponse

app = FastAPI(
    title="API Zeladoria Urbana",
    description="Sistema de registo de problemas urbanos para cidadãos.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def tela():
    return FileResponse(Path(__file__).parent / "static" / "indexx.html")


app.include_router(consultas.router)
app.include_router(ocorrencias.router)
app.include_router(categorias.router)