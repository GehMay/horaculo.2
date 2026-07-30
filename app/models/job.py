from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class ApplicationStatus(str, enum.Enum):
    NOVO = "NOVO"
    EM_ANALISE = "EM_ANALISE"
    ENTREVISTA = "ENTREVISTA"
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    
    requirements = relationship("JobRequirement", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")

class JobRequirement(Base):
    __tablename__ = "job_requirements"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    atributo = Column(String, nullable=False)
    peso_desejado = Column(Integer, nullable=False) # 1 a 5

    job = relationship("Job", back_populates="requirements")

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.NOVO, nullable=False)

    job = relationship("Job", back_populates="applications")
