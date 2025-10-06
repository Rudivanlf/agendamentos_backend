from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo


def sao_paulo_now():
    return datetime.now(tz=ZoneInfo("America/Sao_Paulo"))


class Agendamento(Document):
    # O Field aqui é importante por causa do alias para o "_id" do MongoDB.
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")

    client_name: str
    client_email: EmailStr = Field(...)
    agendamento_date: datetime = Field(default_factory=sao_paulo_now)

    description: Optional[str] = None

    # A Config é necessária apenas para o alias funcionar.
    class Config:
        populate_by_name = True

    class Settings:
        name = "agendamentos"


class UpdateAgendamento(BaseModel):
    # Modelo para update, todos os campos são opcionais.
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    agendamento_date: Optional[datetime] = None
    description: Optional[str] = None
