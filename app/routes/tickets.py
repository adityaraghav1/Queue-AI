import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.database.database import get_db
from app.database.models import Ticket, TicketStatus, User
from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketStatusUpdate,
    TicketFinalResponseUpdate,
)
from app.services.ai_triage import analyze_ticket


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        ai_result = analyze_ticket(
            subject=ticket_data.subject,
            description=ticket_data.description
        )
    except Exception:
        logger.exception("AI ticket analysis failed")
        ai_result = None

    new_ticket = Ticket(
        customer_id=current_user.id,
        subject=ticket_data.subject,
        description=ticket_data.description,
        category=ai_result["category"] if ai_result else None,
        priority=ai_result["priority"] if ai_result else None,
        sentiment=ai_result["sentiment"] if ai_result else None,
        suggested_response=(
            ai_result["suggested_response"] if ai_result else None
        )
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@router.get(
    "/my",
    response_model=list[TicketResponse]
)
def get_my_tickets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tickets = (
        db.query(Ticket)
        .filter(Ticket.customer_id == current_user.id)
        .order_by(Ticket.created_at.desc())
        .all()
    )

    return tickets


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.customer_id == current_user.id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


@router.get(
    "/",
    response_model=list[TicketResponse]
)
def get_all_tickets(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    tickets = (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .all()
    )

    return tickets


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse
)
def update_ticket_status(
    ticket_id: int,
    status_data: TicketStatusUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    ticket.status = status_data.status

    db.commit()
    db.refresh(ticket)

    return ticket


@router.patch(
    "/{ticket_id}/response",
    response_model=TicketResponse
)
def update_ticket_response(
    ticket_id: int,
    response_data: TicketFinalResponseUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    ticket.final_response = response_data.final_response
    ticket.status = TicketStatus.RESOLVED

    db.commit()
    db.refresh(ticket)

    return ticket