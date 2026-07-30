from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models.user import User, RoleEnum
from app.models.event import Event, EventEnrollment, StudentAttribute
from app.schemas.event import EvaluationCreate, QRCodeData
from app.core.security import get_current_user, require_role
from app.config import settings

router = APIRouter(prefix="/api/v1/events", tags=["events"])

@router.post("/{event_id}/enroll")
def enroll_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [RoleEnum.ALUNO, RoleEnum.MENTOR]:
        raise HTTPException(status_code=403, detail="Apenas alunos e mentores podem se inscrever.")
        
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
        
    existing_enrollment = db.query(EventEnrollment).filter(
        EventEnrollment.event_id == event_id,
        EventEnrollment.user_id == current_user.id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Você já está inscrito neste evento.")
        
    current_enrollments_count = db.query(EventEnrollment).join(User).filter(
        EventEnrollment.event_id == event_id,
        User.role == current_user.role
    ).count()
    
    if current_user.role == RoleEnum.ALUNO and current_enrollments_count >= event.vagas_alunos:
        raise HTTPException(status_code=400, detail="Vagas para alunos esgotadas.")
    if current_user.role == RoleEnum.MENTOR and current_enrollments_count >= event.vagas_mentores:
        raise HTTPException(status_code=400, detail="Vagas para mentores esgotadas.")
        
    enrollment = EventEnrollment(event_id=event_id, user_id=current_user.id)
    db.add(enrollment)
    db.commit()
    return {"message": "Inscrição realizada com sucesso."}

@router.get("/{event_id}/qrcode")
def get_qrcode(
    event_id: int,
    current_user: User = Depends(require_role([RoleEnum.ALUNO]))
):
    expire = datetime.now(timezone.utc) + timedelta(seconds=60)
    payload = {
        "user_id": current_user.id,
        "event_id": event_id,
        "exp": expire
    }
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"qr_data": encoded_jwt}

@router.post("/checkin")
def process_checkin(
    data: QRCodeData,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.MENTOR]))
):
    try:
        payload = jwt.decode(data.qr_data, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        aluno_id = payload.get("user_id")
        event_id = payload.get("event_id")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="QR Code expirado.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="QR Code inválido.")
        
    enrollment = db.query(EventEnrollment).filter(
        EventEnrollment.event_id == event_id,
        EventEnrollment.user_id == aluno_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscrição do aluno não encontrada para este evento.")
        
    if enrollment.check_in:
         return {"message": "Check-in já havia sido realizado."}
         
    enrollment.check_in = True
    enrollment.avaliador_id = current_user.id
    db.commit()
    
    return {"message": "Check-in realizado com sucesso."}

@router.post("/{event_id}/evaluate")
def evaluate_student(
    event_id: int,
    eval_data: EvaluationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.MENTOR]))
):
    enrollment = db.query(EventEnrollment).filter(
        EventEnrollment.event_id == event_id,
        EventEnrollment.user_id == eval_data.aluno_id,
        EventEnrollment.avaliador_id == current_user.id,
        EventEnrollment.check_in == True
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=400, detail="Não autorizado a avaliar este aluno ou aluno ausente.")
        
    for item in eval_data.avaliacoes:
        student_attr = StudentAttribute(
            aluno_id=eval_data.aluno_id,
            mentor_id=current_user.id,
            event_id=event_id,
            atributo_nome=item.atributo_nome,
            pontos_obtidos=item.pontos_obtidos,
            feedback=eval_data.feedback
        )
        db.add(student_attr)
        
    db.commit()
    return {"message": "Avaliação salva com sucesso."}
