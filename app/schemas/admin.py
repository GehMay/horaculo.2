from pydantic import BaseModel
from typing import Optional
from app.models.admin import TicketStatus, ProjectStatus

class TicketCreate(BaseModel):
    assunto: str
    mensagem: str

class TicketReply(BaseModel):
    mensagem: str
    novo_status: TicketStatus

class CampaignCreate(BaseModel):
    titulo: str
    imagem_url: str
    link_externo: str
    ativo: bool = True

class ProjectCreate(BaseModel):
    titulo: str
    descricao: str
    valor_estimado: Optional[float] = None
