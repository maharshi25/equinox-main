
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from database import get_db
from database.models import ChatThread
from datetime import datetime

from utils.auth import get_current_user_email

router = APIRouter(prefix="/api/history", tags=["history"])

class ThreadCreate(BaseModel):
    messages: List[Dict[str, Any]]
    title: str = "New Conversation"

@router.post("/{email}/{thread_id}")
def save_thread(
    email: str,
    thread_id: str,
    thread_data: ThreadCreate,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user_email),
):
    """
    Save or update a chat thread.
    thread_id can be any unique string (e.g. hash of timestamp + email).
    """
    if current_user_email.lower() != email.lower():
        raise HTTPException(status_code=403, detail="Thread access is denied for this user")

    existing_thread = db.query(ChatThread).filter(
        ChatThread.id == thread_id,
        ChatThread.user_email == current_user_email,
    ).first()

    if existing_thread:
        existing_thread.messages = thread_data.messages
        existing_thread.title = thread_data.title
    else:
        new_thread = ChatThread(
            id=thread_id,
            user_email=current_user_email,
            title=thread_data.title,
            messages=thread_data.messages,
        )
        db.add(new_thread)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "thread_id": thread_id}

@router.get("/{email}")
def get_user_threads(
    email: str,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user_email),
):
    """Get all threads for a user"""
    if current_user_email.lower() != email.lower():
        raise HTTPException(status_code=403, detail="Thread access is denied for this user")

    threads = db.query(ChatThread).filter(ChatThread.user_email == current_user_email).order_by(ChatThread.created_at.desc()).all()
    return threads

@router.get("/{email}/{thread_id}")
def get_thread(
    email: str,
    thread_id: str,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user_email),
):
    """Get a specific thread"""
    if current_user_email.lower() != email.lower():
        raise HTTPException(status_code=403, detail="Thread access is denied for this user")

    thread = db.query(ChatThread).filter(
        ChatThread.id == thread_id,
        ChatThread.user_email == current_user_email,
    ).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread
