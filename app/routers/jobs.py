from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, RoleEnum
from app.models.job import Job, JobRequirement, JobApplication
from app.schemas.job import JobCreate, JobResponse, ApplicationStatusUpdate
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/api/v1", tags=["jobs"])

@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.EMPRESA]))
):
    new_job = Job(
        empresa_id=current_user.id,
        titulo=job_in.titulo,
        descricao=job_in.descricao
    )
    db.add(new_job)
    db.flush()
    
    for req in job_in.requisitos:
        new_req = JobRequirement(
            job_id=new_job.id,
            atributo=req.atributo,
            peso_desejado=req.peso_desejado
        )
        db.add(new_req)
        
    db.commit()
    db.refresh(new_job)
    return new_job

@router.patch("/applications/{id}/status")
def update_application_status(
    id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.EMPRESA]))
):
    application = db.query(JobApplication).filter(JobApplication.id == id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Candidatura não encontrada.")
    
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job or job.empresa_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para alterar esta candidatura.")
        
    application.status = status_update.status
    db.commit()
    
    return {"message": "Status atualizado com sucesso", "new_status": application.status}
