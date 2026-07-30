from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProfileAlunoUpdate(BaseModel):
    ra: str
    nome_completo: str
    cpf: str
    telefone: str
    data_nascimento: date
    genero: Optional[str] = None
    foto_url: Optional[str] = None

class ProfileEmpresaUpdate(BaseModel):
    razao_social: str
    cnpj: str
    rep_legal_nome: str
    rep_legal_cpf: str
    supervisor_nome: str
    endereco: str

class ProfileMentorUpdate(BaseModel):
    nome_completo: str
    cpf: str
    telefone: str
    data_nascimento: date
    genero: Optional[str] = None
    foto_url: Optional[str] = None
