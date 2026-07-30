from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class EventStatus(str, enum.Enum):
    ABERTO = "ABERTO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    vagas_alunos = Column(Integer, nullable=False)
    vagas_mentores = Column(Integer, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.ABERTO, nullable=False)
    
    attributes = relationship("EventAttribute", back_populates="event", cascade="all, delete-orphan")
    enrollments = relationship("EventEnrollment", back_populates="event", cascade="all, delete-orphan")

class EventAttribute(Base):
    __tablename__ = "event_attributes"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    atributo_nome = Column(String, nullable=False)
    pontos_maximos = Column(Integer, nullable=False)

    event = relationship("Event", back_populates="attributes")

class EventEnrollment(Base):
    __tablename__ = "event_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in = Column(Boolean, default=False, nullable=False)
    avaliador_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    event = relationship("Event", back_populates="enrollments")

class StudentAttribute(Base):
    __tablename__ = "student_attributes"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    atributo_nome = Column(String, nullable=False)
    pontos_obtidos = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=True)
