from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os
import uuid

from app.database import get_db
from app.models.user import User, RoleEnum
from app.models.profile import ProfileAluno, ProfileEmpresa, ProfileMentor
from app.schemas.profile import ProfileAlunoUpdate, ProfileEmpresaUpdate, ProfileMentorUpdate
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.put("/aluno")
def update_profile_aluno(
    profile_in: ProfileAlunoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ALUNO]))
):
    profile = db.query(ProfileAluno).filter(ProfileAluno.user_id == current_user.id).first()
    if profile:
        for var, value in vars(profile_in).items():
            setattr(profile, var, value)
    else:
        profile = ProfileAluno(user_id=current_user.id, **profile_in.model_dump())
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return {"message": "Perfil atualizado com sucesso.", "profile": profile}

@router.put("/empresa")
def update_profile_empresa(
    profile_in: ProfileEmpresaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.EMPRESA]))
):
    profile = db.query(ProfileEmpresa).filter(ProfileEmpresa.user_id == current_user.id).first()
    if profile:
        for var, value in vars(profile_in).items():
            setattr(profile, var, value)
    else:
        profile = ProfileEmpresa(user_id=current_user.id, **profile_in.model_dump())
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return {"message": "Perfil atualizado com sucesso.", "profile": profile}

@router.put("/mentor")
def update_profile_mentor(
    profile_in: ProfileMentorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.MENTOR]))
):
    profile = db.query(ProfileMentor).filter(ProfileMentor.user_id == current_user.id).first()
    if profile:
        for var, value in vars(profile_in).items():
            setattr(profile, var, value)
    else:
        profile = ProfileMentor(user_id=current_user.id, **profile_in.model_dump())
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return {"message": "Perfil atualizado com sucesso.", "profile": profile}

@router.get("/me")
def get_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = None
    if current_user.role == RoleEnum.ALUNO:
        profile = db.query(ProfileAluno).filter(ProfileAluno.user_id == current_user.id).first()
    elif current_user.role == RoleEnum.EMPRESA:
        profile = db.query(ProfileEmpresa).filter(ProfileEmpresa.user_id == current_user.id).first()
    elif current_user.role == RoleEnum.MENTOR:
        profile = db.query(ProfileMentor).filter(ProfileMentor.user_id == current_user.id).first()
        
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    
    return {"user": current_user, "profile": profile}

@router.post("/upload")
def upload_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"url": f"/uploads/images/{filename}"}
