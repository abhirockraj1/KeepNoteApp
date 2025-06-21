from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

import models as pydantic_models  # Pydantic models for request/response
import data as db_schemas    # SQLAlchemy models for database
from core.dependencies import get_db
from services import user_service
from utils import security

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=pydantic_models.User, status_code=status.HTTP_201_CREATED)
def register_user(user: pydantic_models.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_service.create_user(db, user=user)

@router.post("/login", response_model=pydantic_models.Token)
def login_for_access_token(form_data: pydantic_models.UserCreate, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, email=form_data.email)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": str(user.email)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/all/users/")
async def read_users_all(limitU: int , db: Session = Depends(get_db)):
    return {"Emails": user_service.get_users(db,skip=0, limit= limitU)}
