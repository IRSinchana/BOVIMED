"""Persistent in-app notifications with i18n template keys."""

from __future__ import annotations

import logging

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.notification import Notification, NotificationPreference
from app.models.user import User

logger = logging.getLogger(__name__)

# Risk levels that generate in-app notifications (Low/Healthy = no notification).
RISK_NOTIFICATION_TYPES = {
    "Mild": ("MILD_RISK", "notifications.mildRisk", "info"),
    "Moderate": ("MODERATE_RISK", "notifications.moderateRisk", "warning"),
    "High": ("HIGH_RISK", "notifications.highRisk", "high"),
    "Critical": ("CRITICAL_RISK", "notifications.criticalRisk", "critical"),
    "Severe": ("HIGH_RISK", "notifications.highRisk", "high"),
}


def get_or_create_preferences(db: Session, user_id: int) -> NotificationPreference:
    prefs = db.get(NotificationPreference, user_id)
    if prefs:
        return prefs
    prefs = NotificationPreference(user_id=user_id)
    db.add(prefs)
    db.commit()
    db.refresh(prefs)
    return prefs


def _already_notified(db: Session, user_id: int, analysis_id: int) -> bool:
    """Prevent duplicate notifications for the same analysis and user."""
    recent = db.scalars(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(200)
    ).all()
    return any(n.payload.get("analysisId") == analysis_id for n in recent)


def create_analysis_notifications(
    db: Session,
    analysis: Analysis,
    *,
    user_id: int | None = None,
) -> list[Notification]:
    """Create notifications for the logged-in user (or all active users if anonymous)."""
    risk = analysis.risk_level
    mapping = RISK_NOTIFICATION_TYPES.get(risk)
    if not mapping:
        return []

    notif_type, key_prefix, severity = mapping

    if user_id is not None:
        user = db.get(User, user_id)
        users = [user] if user and user.is_active else []
    else:
        users = list(db.scalars(select(User).where(User.is_active.is_(True))).all())

    created: list[Notification] = []

    confidence_pct = round(float(analysis.confidence) * 100, 1)
    if analysis.confidence > 1:
        confidence_pct = round(float(analysis.confidence), 1)

    payload = {
        "cowId": analysis.cow_id,
        "detection": analysis.prediction,
        "confidence": confidence_pct,
        "risk": risk,
        "analysisId": analysis.id,
    }
    action_url = f"/result/{analysis.id}"

    for user in users:
        if _already_notified(db, user.id, analysis.id):
            continue
        prefs = get_or_create_preferences(db, user.id)
        if not prefs.health_alerts:
            continue
        notif = Notification(
            user_id=user.id,
            cow_id=analysis.cow_id,
            type=notif_type,
            title_key=f"{key_prefix}.title",
            message_key=f"{key_prefix}.message",
            payload=payload,
            severity=severity,
            is_read=False,
            action_url=action_url,
        )
        db.add(notif)
        created.append(notif)

    if created:
        db.commit()
        for n in created:
            db.refresh(n)
        logger.info(
            "Created %s notification(s) for analysis %s (risk=%s)",
            len(created),
            analysis.id,
            risk,
        )
    return created


def list_notifications(db: Session, user_id: int, limit: int = 50) -> list[Notification]:
    return list(
        db.scalars(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        ).all()
    )


def unread_count(db: Session, user_id: int) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
        )
        or 0
    )


def mark_read(db: Session, user_id: int, notification_id: int) -> Notification | None:
    notif = db.get(Notification, notification_id)
    if not notif or notif.user_id != user_id:
        return None
    notif.is_read = True
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def mark_all_read(db: Session, user_id: int) -> int:
    result = db.execute(
        update(Notification)
        .where(Notification.user_id == user_id, Notification.is_read.is_(False))
        .values(is_read=True)
    )
    db.commit()
    return int(result.rowcount or 0)
