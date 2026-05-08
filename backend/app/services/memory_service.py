from sqlalchemy.orm import Session

from app.models.chat import ChatMessage, ChatSession


def create_session(db: Session, title: str | None = None) -> ChatSession:
    chat_session = ChatSession(title=title)
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    return chat_session


def get_session(db: Session, session_id: str) -> ChatSession | None:
    return (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )


def save_message(
    db: Session,
    session_id: str,
    role: str,
    content: str,
    metadata_json: dict | None = None,
) -> ChatMessage:
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        metadata_json=metadata_json,
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, session_id: str, limit: int = 20) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )[::-1]
    
def build_conversation_context(messages: list[ChatMessage]) -> str:
    if not messages:
        return ""

    context_lines = []

    for message in messages:
        role = "User" if message.role == "user" else "CyberGuard"
        context_lines.append(f"{role}: {message.content}")

    return "\n".join(context_lines)