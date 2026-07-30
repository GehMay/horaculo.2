from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User, RoleEnum, StatusEnum
from app.models.admin import Ticket, Campaign, FecapTechProject, TicketStatus
from app.schemas.admin import TicketCreate, TicketReply, CampaignCreate, ProjectCreate
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

@router.get("/users/pending")
def list_pending_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.FECAP]))
):
    users = db.query(User).filter(User.status == StatusEnum.PENDENTE).all()
    return users

@router.patch("/users/{user_id}/approve")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.FECAP]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
    user.status = StatusEnum.ATIVO
    db.commit()
    return {"message": "Usuário aprovado com sucesso."}

@router.get("/tickets")
def list_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.FECAP]))
):
    return db.query(Ticket).all()

@router.post("/tickets/{ticket_id}/reply")
def reply_ticket(
    ticket_id: int,
    reply: TicketReply,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.FECAP]))
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")
        
    ticket.status = reply.novo_status
    db.commit()
    return {"message": "Resposta enviada e status atualizado."}

@router.post("/campaigns")
def create_campaign(
    campaign_in: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.FECAP]))
):
    new_campaign = Campaign(**campaign_in.model_dump())
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@router.post("/projects")
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.FECAP]))
):
    new_project = FecapTechProject(**project_in.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project
