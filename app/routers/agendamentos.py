from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId # ID especial do Beanie

from ..models.agendamento import Agendamento, UpdateAgendamento

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)

@router.post("/", response_model=Agendamento, status_code=status.HTTP_201_CREATED)
async def criar_agendamento(agendamento: Agendamento):
    await agendamento.create()
    return agendamento

@router.get("/", response_model=List[Agendamento])
async def listar_agendamentos():
    return await Agendamento.find_all().to_list()

@router.get("/{id}", response_model=Agendamento)
async def obter_agendamento(id: PydanticObjectId):
    agendamento = await Agendamento.get(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento

@router.put("/{id}", response_model=Agendamento)
async def atualizar_agendamento(id: PydanticObjectId, update_data: UpdateAgendamento):
    agendamento = await Agendamento.get(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    update = update_data.model_dump(exclude_unset=True)
    await agendamento.update({"$set": update})
    return await Agendamento.get(id) 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_agendamento(id: PydanticObjectId):
    agendamento = await Agendamento.get(id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    await agendamento.delete()