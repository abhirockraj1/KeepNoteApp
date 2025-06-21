from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .config import settings
import data as db_schemas
import models as pydantic_models
from services import user_service
from .database import get_db  # Corrected import: relative import

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str  = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = pydantic_models.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user
