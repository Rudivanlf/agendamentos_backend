from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List
from beanie import PydanticObjectId  # ID especial do Beanie
from datetime import datetime

from ..models.agendamento import Agendamento, UpdateAgendamento
from ..services.email import send_agendamento_confirmation

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)


@router.post("/", response_model=Agendamento, status_code=status.HTTP_201_CREATED)
async def criar_agendamento(agendamento: Agendamento, background_tasks: BackgroundTasks):
    await agendamento.create()

    # 1. Formata a data para ser legível no email
    formatted_date = agendamento.agendamento_date.astimezone(None).strftime("%d/%m/%Y às %H:%M:%S")

    background_tasks.add_task(
        send_agendamento_confirmation, 
        agendamento.client_email, 
        agendamento.client_name,  
        formatted_date            
    )

    return agendamento


@router.get("/", response_model=List[Agendamento])
async def listar_agendamentos():
    return await Agendamento.find_all().to_list()


@router.get("/{id}", response_model=Agendamento)
async def obter_agendamento(id: PydanticObjectId):
    agendamento = await Agendamento.get(id)
    if not agendamento:
        raise HTTPException(
            status_code=404, detail="Agendamento não encontrado")
    return agendamento


@router.put("/{id}", response_model=Agendamento)
async def atualizar_agendamento(id: PydanticObjectId, update_data: UpdateAgendamento):
    agendamento = await Agendamento.get(id)
    if not agendamento:
        raise HTTPException(
            status_code=404, detail="Agendamento não encontrado")

    update = update_data.model_dump(exclude_unset=True)
    await agendamento.update({"$set": update})
    return await Agendamento.get(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_agendamento(id: PydanticObjectId):
    agendamento = await Agendamento.get(id)
    if not agendamento:
        raise HTTPException(
            status_code=404, detail="Agendamento não encontrado")

    await agendamento.delete()
