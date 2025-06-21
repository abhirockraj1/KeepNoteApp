from sqlalchemy.orm import Session
import models as pydantic_models  # Pydantic models for data validation
import data as db_schemas    # SQLAlchemy models for database interaction
from services import user_service

def create_node_file(db: Session, note: pydantic_models.NoteFileCreate, email: str):
    db_file = db_schemas.NoteFile(email= email, title = note.title, content= note.content)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def update_node_file(db: Session, email , Note: pydantic_models.NoteFileCreate):
    db_file = db.query(db_schemas.NoteFile).filter(db_schemas.NoteFile.email == email , db_schemas.NoteFile.title == Note.title).first()
    if db_file:
        for key, value in Note.model_dump(exclude_unset=True).items():
            setattr(db_file, key, value)
        db.commit()
        db.refresh(db_file)
    return db_file

def delete_Node_file(db: Session, email ,title):
    db_file = db.query(db_schemas.NoteFile).filter(db_schemas.NoteFile.email == email
    ,db_schemas.NoteFile.title == title).first()
    if db_file:
        db.delete(db_file)
        db.commit()
        return True
    return False

def get_node_file(db: Session, email: str, title: str):
    return db.query(db_schemas.NoteFile).filter(
        db_schemas.NoteFile.email == email,
        db_schemas.NoteFile.title == title).first()

def get_all_node_files(db: Session, email: str, skip: int = 0, limit: int = 1000):
    return db.query(db_schemas.NoteFile).filter(db_schemas.NoteFile.email == email).offset(skip).limit(limit).all()
     
# 