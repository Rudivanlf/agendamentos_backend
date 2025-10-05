import motor.motor_asyncio
from ..core.config import settings

# Cria uma instância do cliente do MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)

# Acessa o banco de dados.
db = client.agendamentos_db

# Acessa a coleção (tabela) de agendamentos
AppointmentCollection = db.get_collection("agendamentos")