from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class TicketStatus(str, enum.Enum):
    ABERTO = "ABERTO"
    EM_ATENDIMENTO = "EM_ATENDIMENTO"
    RESOLVIDO = "RESOLVIDO"

class ProjectStatus(str, enum.Enum):
    DISPONIVEL = "DISPONIVEL"
    NEGOCIACAO = "NEGOCIACAO"
    VENDIDO = "VENDIDO"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assunto = Column(String, nullable=False)
    mensagem = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.ABERTO, nullable=False)

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    imagem_url = Column(String, nullable=False)
    link_externo = Column(String, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

class FecapTechProject(Base):
    __tablename__ = "fecap_tech_projects"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    valor_estimado = Column(Float, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DISPONIVEL, nullable=False)
