from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class SupportSubject(Base):
    __tablename__ = "support_subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    priority = Column(Integer, default=1, nullable=False)

    tickets = relationship("SupportTicket", back_populates="subject")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("support_subjects.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String, default="open", nullable=False, index=True, comment="open, closed, pending")
    resolved_at = Column(DateTime, default=None, nullable=True)  # Adjusted for clarity
    assignee = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for unassigned tickets

    user = relationship("User", back_populates="tickets", foreign_keys=[user_id])
    support_agent = relationship("User", back_populates="assigned_tickets", foreign_keys=[assignee])
    subject = relationship("SupportSubject", back_populates="tickets")
    messages = relationship("SupportMessages", back_populates="ticket")

class SupportMessages(Base):
    __tablename__ = "support_messages"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    admin_response = Column(Boolean, default=False)

    ticket = relationship("SupportTicket", back_populates="messages")
    user = relationship("User", back_populates="ticket_messages")


class SupportSubjectCreate(BaseModel):
    name: str
    priority: int


class SupportTicketCreate(BaseModel):
    subject_id: int
    message: str


class SupportMessagesCreate(BaseModel):
    ticket_id: int
    message: str


class SupportTicketUpdate(BaseModel):
    subject_id: Optional[int] = None
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None
    assignee: Optional[int] = None


class SupportSubjectUpdate(BaseModel):
    name: Optional[str] = None
    priority: Optional[int] = None


class SupportTicketResponse(BaseModel):
    id: int
    user_id: int
    subject_id: int
    message: str
    created_at: datetime
    status: str
    resolved_at: Optional[datetime] = None
    assignee: Optional[int] = None


class SupportSubjectResponse(BaseModel):
    id: int
    name: str
    priority: int


class SupportMessagesResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    message: str
    created_at: datetime
    admin_response: bool
