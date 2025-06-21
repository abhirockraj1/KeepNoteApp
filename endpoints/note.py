from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models as pydantic_models
import data as db_schemas
from core.dependencies import get_db,  get_current_user
from services import note

router = APIRouter(prefix="/notes", tags=["node_files"])

@router.post("/", response_model=pydantic_models.NoteFile, status_code=status.HTTP_201_CREATED)
def create_file(
    noteU: pydantic_models.NoteFileCreate, 
    db: Session = Depends(get_db), 
    current_user: db_schemas.User = Depends(get_current_user)):
    if note.get_node_file(db,current_user.email, noteU.title ) is None:
        return note.create_node_file(db, noteU, current_user.email)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Note already present plz update if needed ")

@router.get("/{title}", response_model=pydantic_models.NoteFile)
def read_file(title:str, db: Session = Depends(get_db), current_user: db_schemas.User = Depends(get_current_user)):
    noteInfo = note.get_node_file(db,current_user.email, title )
    if noteInfo is not None:
        return noteInfo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not present")
# 

@router.get("/v1/all")
def read_all_file(
    db: Session = Depends(get_db),
    current_user: db_schemas.User = Depends(get_current_user)
):
    return {"Notes": note.get_all_node_files(db, current_user.email )}

@router.put("/update", response_model=pydantic_models.NoteFile)
def update_file(
    note_update: pydantic_models.NoteFileCreate,
    db: Session = Depends(get_db),
    current_user: db_schemas.User = Depends(get_current_user)
):
    db_file = note.get_node_file(db, email= current_user.email, title= note_update.title )
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if db_file.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this file")
    note.update_node_file(db, current_user.email, note_update)
    return note.get_node_file(db,current_user.email, note_update.title )

@router.delete("/{title}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    title: str,
    db: Session = Depends(get_db),
    current_user: db_schemas.User = Depends(get_current_user)
):
    db_file = note.get_node_file(db, email= current_user.email, title= title )
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if db_file.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this file")
    note.delete_Node_file(db, current_user.email, title= title)
    # raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete Note")
