from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import consultas, ocorrencias, categorias
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

STATIC = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")

@app.get("/", include_in_schema=False)
def tela():
    return FileResponse(STATIC / "index.html")

app.include_router(consultas.router)
app.include_router(ocorrencias.router)
app.include_router(categorias.router)