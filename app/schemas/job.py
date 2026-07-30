from pydantic import BaseModel
from typing import List
from app.models.job import ApplicationStatus

class JobRequirementCreate(BaseModel):
    atributo: str
    peso_desejado: int

class JobCreate(BaseModel):
    titulo: str
    descricao: str
    requisitos: List[JobRequirementCreate]

class JobResponse(BaseModel):
    id: int
    empresa_id: int
    titulo: str
    descricao: str
    
    class Config:
        from_attributes = True

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
