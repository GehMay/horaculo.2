from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base

class RoleEnum(str, enum.Enum):
    FECAP = "FECAP"
    ALUNO = "ALUNO"
    EMPRESA = "EMPRESA"
    MENTOR = "MENTOR"

class StatusEnum(str, enum.Enum):
    PENDENTE = "PENDENTE"
    ATIVO = "ATIVO"
    BLOQUEADO = "BLOQUEADO"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDENTE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
