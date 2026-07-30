from pydantic import BaseModel
from typing import List, Optional

class AttributeEvaluation(BaseModel):
    atributo_nome: str
    pontos_obtidos: int

class EvaluationCreate(BaseModel):
    aluno_id: int
    avaliacoes: List[AttributeEvaluation]
    feedback: Optional[str] = None

class QRCodeData(BaseModel):
    qr_data: str
