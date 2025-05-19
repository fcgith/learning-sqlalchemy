from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("support_subjects"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String, default="waiting")
    resolved_at = Column(DateTime, default=None)
    assignee = Column(Integer, ForeignKey("users.id"), default=None)

    user = relationship("User", back_populates="tickets")
    support_agent = relationship("User", back_populates="agent")
    subject = relationship("SupportSubject", back_populates="tickets")
    messages = relationship("SupportMessages", back_populates="ticket")


class SupportSubject(Base):
    __tablename__ = "support_subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    priority = Column(Integer, default=1, nullable=False)

    tickets = relationship("SupportTicket", back_populates="subject")


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
    id: str
    name: str
    priority: int



class SupportTicketCreate(BaseModel):
    user_id: int
    subject_id: str
    message: str


class SupportMessagesCreate(BaseModel):
    ticket_id: int
    user_id: int
    message: str
    admin_response: bool = False


class SupportAdminMessageCreate(BaseModel):
    ticket_id: int
    user_id: int
    message: str
    admin_response: bool = True


class SupportTicketUpdate(BaseModel):
    subject_id: Optional[int] = None
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None
    assignee: Optional[int] = None


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
