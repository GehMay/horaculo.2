from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base

class ProfileAluno(Base):
    __tablename__ = "profiles_aluno"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    ra = Column(String, unique=True, nullable=False)
    nome_completo = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    genero = Column(String)
    foto_url = Column(String)

class ProfileEmpresa(Base):
    __tablename__ = "profiles_empresa"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    razao_social = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    rep_legal_nome = Column(String, nullable=False)
    rep_legal_cpf = Column(String, nullable=False)
    supervisor_nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

class ProfileMentor(Base):
    __tablename__ = "profiles_mentor"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    nome_completo = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    genero = Column(String)
    foto_url = Column(String)
