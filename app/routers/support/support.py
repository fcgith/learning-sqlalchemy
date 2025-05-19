import http
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import get_db, get_current_user, get_current_admin
from app.models.support import SupportTicketResponse, SupportTicketCreate, SupportTicketUpdate, SupportMessagesResponse, \
    SupportMessagesCreate, SupportSubjectResponse, SupportSubjectCreate, SupportSubjectUpdate
import app.services.ticket_services as ticket_services
from app.services import support_services

router = APIRouter()


@router.post("/subjects", response_model=SupportSubjectResponse)
def create_support_subject(subject: SupportSubjectCreate,
                           db: Session = Depends(get_db),
                           admin: User = Depends(get_current_admin)):
    """Create a new support subject"""
    return support_services.create_support_subject(db, subject)


@router.get("/subjects", response_model=List[SupportSubjectResponse])
def get_support_subjects(db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Retrieve all support subjects"""
    return support_services.get_all_support_subjects(db)


@router.get("/subjects/{subject_id}", response_model=SupportSubjectResponse)
def get_support_subject(subject_id: int, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    """Retrieve a support subject by ID"""
    return support_services.get_support_subject_by_id(db, subject_id)


@router.put("/subjects/{subject_id}", response_model=SupportSubjectResponse)
def update_support_subject(subject_id: int,
                           subject: SupportSubjectUpdate,
                           db: Session = Depends(get_db),
                           admin: User = Depends(get_current_admin)):
    """Update a support subject"""
    return support_services.update_support_subject(db, subject_id, subject)


@router.delete("/subjects/{subject_id}", status_code=http.HTTPStatus.NO_CONTENT.value)
def delete_support_subject(subject_id: int,
                           db: Session = Depends(get_db),
                           admin: User = Depends(get_current_admin)):
    """Delete a support subject"""
    return support_services.delete_support_subject(db, subject_id)


@router.post("/", response_model=SupportTicketResponse)
def create_support_ticket(ticket: SupportTicketCreate,
                          db: Session = Depends(get_db),
                          user: User = Depends(get_current_user)):
    """Create a new support ticket"""
    return ticket_services.create_ticket(db, ticket, user)


@router.post("/{ticket_id}/assign", response_model=SupportTicketResponse)
def assign_ticket(ticket_id: int,
                  assignee_id: int,
                  db: Session = Depends(get_db),
                  admin: User = Depends(get_current_admin)):
    """Assign a ticket to an agent"""
    return ticket_services.assign_ticket(db, ticket_id, assignee_id)


@router.get("/", response_model=List[SupportTicketResponse])
def get_all_support_tickets(db: Session = Depends(get_db),
                            admin: User = Depends(get_current_admin)):
    """Retrieve all support tickets"""
    return ticket_services.get_all_tickets(db)


@router.get("/my-tickets", response_model=List[SupportTicketResponse])
def get_my_tickets(db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    """Retrieve the current user's support tickets"""
    return ticket_services.get_my_ticket(db, user)


@router.get("/assignee/{assignee_id}", response_model=List[SupportTicketResponse])
def get_tickets_by_assignee(assignee_id: int,
                            db: Session = Depends(get_db),
                            admin: User = Depends(get_current_admin)):
    """Retrieve support tickets by assignee"""
    return ticket_services.get_tickets_by_assignee(db, assignee_id)


@router.get("/status/{status}", response_model=List[SupportTicketResponse])
def get_tickets_by_status(status: str,
                          db: Session = Depends(get_db),
                          admin: User = Depends(get_current_admin)):
    """Retrieve support tickets by status"""
    return ticket_services.get_tickets_by_status(db, status)


# 2. Individual Ticket Operations
@router.get("/{ticket_id}", response_model=SupportTicketResponse)
def get_support_ticket(ticket_id: int,
                       db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    """Retrieve a support ticket by ID"""
    return ticket_services.get_ticket_by_id(db, ticket_id)


@router.patch("/{ticket_id}", response_model=SupportTicketResponse)
def partial_update_support_ticket(ticket_id: int,
                                  ticket_update: SupportTicketUpdate,
                                  db: Session = Depends(get_db),
                                  admin: User = Depends(get_current_admin)):
    """Update a support ticket"""
    return ticket_services.update_ticket(db, ticket_id, ticket_update)


@router.delete("/{ticket_id}", status_code=http.HTTPStatus.NO_CONTENT.value,)
def delete_support_ticket(ticket_id: int,
                          db: Session = Depends(get_db),
                          admin: User = Depends(get_current_admin)):
    """Delete a support ticket"""
    return ticket_services.delete_ticket(db, ticket_id)



# 3. Message Operations
@router.post("/{ticket_id}/messages/", response_model=SupportMessagesResponse)
def create_support_message(ticket_id: int,
                           message: SupportMessagesCreate,
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    """Create a new message in a support ticket"""# Set based on user role
    return ticket_services.create_support_message(db, message, user)


@router.get("/{ticket_id}/messages/", response_model=List[SupportMessagesResponse])
def get_support_messages(ticket_id: int,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Retrieve all messages for a support ticket"""
    return ticket_services.get_support_messages(db, ticket_id, user)
