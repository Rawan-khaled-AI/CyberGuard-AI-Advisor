from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.chat_service import handle_chat_message
from app.services.memory_service import (
    build_conversation_context,
    create_session,
    get_messages,
    get_session,
    save_message,
)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("/")
def chat(data: ChatRequest, db: Session = Depends(get_db)):
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if data.session_id:
        chat_session = get_session(db, data.session_id)

        if chat_session is None:
            raise HTTPException(status_code=404, detail="Chat session not found")
    else:
        title = data.message[:60]
        chat_session = create_session(db, title=title)

    previous_messages = get_messages(db, chat_session.id, limit=10)
    conversation_context = build_conversation_context(previous_messages)

    save_message(
        db=db,
        session_id=chat_session.id,
        role="user",
        content=data.message,
    )

    response = handle_chat_message(
        message=data.message,
        conversation_context=conversation_context,
    )

    assistant_text = (
        response.get("assistant_reply")
        or response.get("answer")
        or str(response)
    )

    save_message(
        db=db,
        session_id=chat_session.id,
        role="assistant",
        content=assistant_text,
        metadata_json=response,
    )

    return {
        "session_id": chat_session.id,
        "response": response,
    }


@router.get("/{session_id}")
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    chat_session = get_session(db, session_id)

    if chat_session is None:
        raise HTTPException(status_code=404, detail="Chat session not found")

    messages = get_messages(db, session_id)

    return {
        "session_id": session_id,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }