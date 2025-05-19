from fastapi import HTTPException
from sqlalchemy.orm import Session
import app.common.errors as e
from app.models.support import SupportTicketCreate, SupportTicket, SupportTicketUpdate, SupportMessages, \
    SupportMessagesCreate
from app.models.user import User


def create_ticket(db: Session, ticket: SupportTicketCreate, user: User):
    ticket = SupportTicket(user_id=user.id, subject_id=ticket.subject_id, message=ticket.message)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_all_tickets(db: Session):
    return db.query(SupportTicket).all()


def get_ticket_by_id(db: Session, ticket_id: int):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


def get_my_ticket(db: Session, user: User):
    return db.query(SupportTicket).filter(SupportTicket.user_id == user.id).all()


def get_tickets_by_assignee(db: Session, assignee_id: int):
    assignee = db.query(SupportTicket).filter(SupportTicket.assignee == assignee_id).all()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    tickets = []
    for ticket in assignee:
        tickets.append(ticket)
    return tickets


def assign_support_ticket(db: Session, ticket_id: int, assignee_id: int):
    """Assign a support ticket to an agent"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    assignee = db.query(User).filter(User.id == assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    ticket.assignee = assignee_id
    db.commit()
    db.refresh(ticket)
    return ticket


def assign_ticket(db, ticket_id, assignee_id):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.assignee = assignee_id
    db.commit()
    db.refresh(ticket)
    return ticket


def get_tickets_by_status(db: Session, status: str):
    tickets = db.query(SupportTicket).filter(SupportTicket.status == status).all()
    return tickets


def update_ticket(db: Session, ticket_id: int, ticket_update: SupportTicketUpdate):
    ticket = get_ticket_by_id(db, ticket_id)
    if ticket_update.status is not None:
        ticket.status = ticket_update.status
    if ticket_update.assignee is not None:
        ticket.assignee = ticket_update.assignee
    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int):
    ticket = get_ticket_by_id(db, ticket_id)
    db.delete(ticket)
    db.commit()
    return True


def create_support_message(db: Session, ticket_id:int, message: SupportMessagesCreate, user):
    ticket = get_ticket_by_id(db, message.ticket_id)
    message = SupportMessages(ticket_id=ticket_id, message=message.message, user_id=user.id)
    if user.admin:
        message.admin_response = True
    ticket.messages.append(message)
    db.commit()
    db.refresh(ticket)
    return message


def get_support_messages(db: Session, ticket_id: int, user: User):
    ticket = get_ticket_by_id(db, ticket_id)
    if ticket.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return ticket.messages