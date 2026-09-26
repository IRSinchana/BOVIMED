"""Chat API."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat import ChatMessage
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.chat_service import get_chat_service

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatContext(BaseModel):
    risk_level: str | None = None
    detection: str | None = None
    prediction: str | None = None
    confidence: float | None = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    language: str = "en"
    cow_id: str | None = None
    context: ChatContext | None = None


class ChatResponse(BaseModel):
    answer: str
    language: str
    sources: list = Field(default_factory=list)
    safety_notice: bool = True
    mode: str = "fallback"


@router.post("", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = get_chat_service()
    ctx = payload.context.model_dump() if payload.context else None
    result = service.reply(
        payload.message,
        language=payload.language,
        cow_id=payload.cow_id,
        context=ctx,
        user_id=current_user.id,
    )

    try:
        db.add(
            ChatMessage(
                user_id=current_user.id,
                cow_id=payload.cow_id,
                language=payload.language,
                role="user",
                message=payload.message,
            )
        )
        db.add(
            ChatMessage(
                user_id=current_user.id,
                cow_id=payload.cow_id,
                language=result.get("language") or payload.language,
                role="assistant",
                message=result["answer"],
            )
        )
        db.commit()
    except Exception:  # noqa: BLE001
        db.rollback()

    return ChatResponse(
        answer=result["answer"],
        language=result.get("language") or payload.language,
        sources=result.get("sources") or [],
        safety_notice=True,
        mode=result.get("mode") or "fallback",
    )


@router.get("/history")
def get_chat_history(
    cow_id: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select

    stmt = (
        select(ChatMessage)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    if cow_id:
        stmt = stmt.where(ChatMessage.cow_id == cow_id)
    messages = db.scalars(stmt).all()
    # Return chronological
    return [
        {
            "id": m.id,
            "role": m.role,
            "message": m.message,
            "language": m.language,
            "cow_id": m.cow_id,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in reversed(messages)
    ]


@router.delete("/history")
def clear_chat_history(
    cow_id: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import delete

    stmt = delete(ChatMessage).where(ChatMessage.user_id == current_user.id)
    if cow_id:
        stmt = stmt.where(ChatMessage.cow_id == cow_id)
    db.execute(stmt)
    db.commit()
    return {"success": True, "message": "Chat history cleared."}
