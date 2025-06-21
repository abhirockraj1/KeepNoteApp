from pydantic import BaseModel
from datetime import datetime

class NoteFile(BaseModel):
    id: int
    email: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NoteFileCreate(BaseModel):
    title: str
    content: str | None = None

class NoteFiledelete(BaseModel):
    title: str
