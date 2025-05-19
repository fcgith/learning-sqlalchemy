from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import get_db, get_current_user, get_current_admin
from app.models.support import SupportTicketResponse, SupportTicketCreate, SupportTicketUpdate, SupportMessagesResponse, \
    SupportMessagesCreate

router = APIRouter(prefix="/support")

@router.post("/", response_model=SupportTicketResponse)
def create_support_ticket(ticket: SupportTicketCreate, db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Create a new support ticket"""
    pass

@router.get("/", response_model=List[SupportTicketResponse])
def get_all_support_tickets(db: Session = Depends(get_db),
                            admin: User = Depends(get_current_admin)):
    """Retrieve all support tickets"""
    pass

@router.get("/my-tickets", response_model=List[SupportTicketResponse])
def get_my_tickets(db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    """Retrieve the current user's support tickets"""
    pass

@router.get("/assignee/{assignee_id}", response_model=List[SupportTicketResponse])
def get_tickets_by_assignee(assignee_id: int, db: Session = Depends(get_db),
                            admin: User = Depends(get_current_admin)):
    """Retrieve support tickets by assignee"""
    pass

@router.get("/status/{status}", response_model=List[SupportTicketResponse])
def get_tickets_by_status(status: str, db: Session = Depends(get_db),
                          admin: User = Depends(get_current_admin)):
    """Retrieve support tickets by status"""
    return get_tickets_by_status(db, status)

# 2. Individual Ticket Operations
@router.get("/{ticket_id}", response_model=SupportTicketResponse)
def get_support_ticket(ticket_id: int, db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    """Retrieve a support ticket by ID"""
    pass

@router.put("/{ticket_id}", response_model=SupportTicketResponse)
def update_support_ticket(ticket_id: int, ticket_update: SupportTicketUpdate,
                         db: Session = Depends(get_db),
                         admin: User = Depends(get_current_admin)):
    """Update a support ticket"""
    return update_support_ticket(db, ticket_id, ticket_update)

@router.patch("/{ticket_id}", response_model=SupportTicketResponse)
def partial_update_support_ticket(ticket_id: int, ticket_update: SupportTicketUpdate,
                                  db: Session = Depends(get_db),
                                  admin: User = Depends(get_current_admin)):
    """Partially update a support ticket"""
    return partial_update_support_ticket(db, ticket_id, ticket_update)

@router.delete("/{ticket_id}")
def delete_support_ticket(ticket_id: int, db: Session = Depends(get_db),
                          admin: User = Depends(get_current_admin)):
    """Delete a support ticket"""
    return delete_support_ticket(db, ticket_id)

@router.post("/{ticket_id}/assign", response_model=SupportTicketResponse)
def assign_support_ticket(ticket_id: int, assignee_id: int,
                         db: Session = Depends(get_db),
                         admin: User = Depends(get_current_admin)):
    """Assign a support ticket to an agent"""
    return assign_support_ticket(db, ticket_id, assignee_id)

# 3. Message Operations
@router.post("/{ticket_id}/messages/", response_model=SupportMessagesResponse)
def create_support_message(ticket_id: int, message: SupportMessagesCreate,
                          db: Session = Depends(get_db),
                          user: User = Depends(get_current_user)):
    """Create a new message in a support ticket"""
    message_data = message.dict(exclude={"ticket_id", "user_id"})  # Ignore client-provided ticket_id, user_id
    message_data["ticket_id"] = ticket_id
    message_data["user_id"] = user.id
    message_data["admin_response"] = user.admin  # Set based on user role
    return create_support_message(db, message_data)

@router.get("/{ticket_id}/messages/", response_model=List[SupportMessagesResponse])
def get_support_messages(ticket_id: int, db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Retrieve all messages for a support ticket"""
    pass