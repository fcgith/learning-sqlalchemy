from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import get_db, get_current_user, get_current_admin
from app.models.support import SupportSubjectResponse, SupportSubjectCreate

router = APIRouter()


@router.post("/", response_model=SupportSubjectResponse)
def create_support_subject(subject: SupportSubjectCreate, db: Session = Depends(get_db),
                           admin: User = Depends(get_current_admin)):
    """Create a new support subject"""
    pass


@router.get("/", response_model=List[SupportSubjectResponse])
def get_support_subjects(db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    """Retrieve all support subjects"""
    pass


@router.get("/{subject_id}", response_model=SupportSubjectResponse)
def get_support_subject(subject_id: int, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    """Retrieve a support subject by ID"""
    pass


@router.put("/{subject_id}", response_model=SupportSubjectResponse)
def update_support_subject(subject_id: int, subject: SupportSubjectCreate,
                           db: Session = Depends(get_db),
                           admin: User = Depends(get_current_admin)):
    """Update a support subject"""
    pass


@router.delete("/{subject_id}")
def delete_support_subject(subject_id: int, db: Session = Depends(get_db),
                           admin: User = Depends(get_current_admin)):
    """Delete a support subject"""
    pass
