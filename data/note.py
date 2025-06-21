from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Table
from sqlalchemy.orm import relationship

from core.database import Base

class NoteFile(Base):
    __tablename__ = "Note_files"

    id = Column(Integer, primary_key=True, index=True) # Added a primary key for NoteFile
    email = Column(String, ForeignKey("users.email"), index=True) # Corrected ForeignKey to users.email
    title = Column(String, unique=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # This defines the relationship from NoteFile to User
    owner = relationship("User", back_populates="owned_notes")
