from sqlalchemy.orm import Session
import app.common.errors as e
from app.models.support import SupportSubjectCreate, SupportSubject, SupportSubjectUpdate


def create_support_subject(db: Session, subject: SupportSubjectCreate):
    sub = db.query(SupportSubject).filter(SupportSubject.name == subject.name).first()
    if sub:
        raise e.invalid_request("Subject already exists")

    db_subject = SupportSubject(name=subject.name, priority=subject.priority)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_all_support_subjects(db: Session):
    return db.query(SupportSubject).all()

def get_support_subject_by_id(db: Session, subject_id: int):
    subject = db.query(SupportSubject).filter(SupportSubject.id == subject_id).first()
    if not subject:
        raise e.no_resource("Subject not found")
    return subject

def update_support_subject(db: Session, subject_id: int, subject: SupportSubjectUpdate):
    sub = get_support_subject_by_id(db, subject_id)
    sub.name = subject.name
    sub.priority = subject.priority
    db.commit()
    db.refresh(sub)
    return sub

def delete_support_subject(db: Session, subject_id: int):
    sub = get_support_subject_by_id(db, subject_id)
    db.delete(sub)
    db.commit()