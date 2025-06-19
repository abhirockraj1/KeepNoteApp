from sqlalchemy.orm import Session
import models as pydantic_models  # Pydantic models for data validation
import data as db_schemas    # SQLAlchemy models for database interaction
from utils import security

def get_user(db: Session, user_id: int):
    return db.query(db_schemas.User).filter(db_schemas.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(db_schemas.User).filter(db_schemas.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    query_results_tuples = db.query(db_schemas.User.email).offset(skip).limit(limit).all()
    return [email_tuple[0] for email_tuple in query_results_tuples]
    

def create_user(db: Session, user: pydantic_models.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = db_schemas.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user