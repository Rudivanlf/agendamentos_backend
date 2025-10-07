from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .core.config import settings
from .models.agendamento import Agendamento
from .routers import agendamentos
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esta função será executada quando a aplicação iniciar
    print("Iniciando a aplicação...")
    client = AsyncIOMotorClient(settings.MONGO_URL)

    await init_beanie(
        database=client.get_database("agendamentos_db"),
        document_models=[Agendamento]  # Lista de todos os seus modelos Beanie
    )
    print("Conexão com o MongoDB estabelecida e Beanie inicializado.")

    yield

    print("Finalizando a aplicação...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agendamentos.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API de Agendamentos"}
