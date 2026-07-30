from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.admin import Ticket, Campaign, FecapTechProject
from app.schemas.admin import TicketCreate
from app.core.security import get_current_user

router = APIRouter(prefix="/api/v1", tags=["showcase"])

@router.get("/showcase")
def get_showcase(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaigns = db.query(Campaign).filter(Campaign.ativo == True).all()
    projects = db.query(FecapTechProject).all()
    
    return {
        "campaigns": campaigns,
        "projects": projects
    }

@router.post("/tickets")
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_ticket = Ticket(
        user_id=current_user.id,
        assunto=ticket_in.assunto,
        mensagem=ticket_in.mensagem
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket
