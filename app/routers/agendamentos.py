from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List
from beanie import PydanticObjectId
from datetime import datetime

# Modelos
from ..models.agendamento import Agendamento, UpdateAgendamento

# A IMPORTAÇÃO CORRETA E FINAL
from ..services.email import send_appointment_confirmation

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)


@router.post("/", response_model=Agendamento, status_code=status.HTTP_201_CREATED)
async def criar_agendamento(agendamento: Agendamento, background_tasks: BackgroundTasks):
    await agendamento.create()

    # Formata a data para ser legível no email
    formatted_date = agendamento.agendamento_date.astimezone(None).strftime("%d/%m/%Y às %H:%M")

    # A CHAMADA DA FUNÇÃO CORRETA E FINAL
    background_tasks.add_task(
        send_appointment_confirmation, 
        agendamento.client_email, 
        agendamento.client_name,  
        formatted_date,          
        agendamento.descricao
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
    # Beanie V2.0+ retorna o documento atualizado
    return await Agendamento.get(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_agendamento(id: PydanticObjectId):
    agendamento = await Agendamento.get(id)
    if not agendamento:
        raise HTTPException(
            status_code=404, detail="Agendamento não encontrado")

    await agendamento.delete()
    return None