"""Authentication and notification center tests."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.database.session import SessionLocal, init_db
from app.models.notification import Notification
from app.models.user import User
from app.services.auth_service import create_access_token
from app.services.notification_service import (
    create_analysis_notifications,
    get_or_create_preferences,
)


@pytest.fixture
def db():
    init_db()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def demo_user(db):
    user = db.scalar(select(User).where(User.mobile == "9876543210"))
    assert user is not None, "Demo farmer must exist (run init_db seed)."
    return user


@pytest.fixture
def health_alerts_enabled(db, demo_user):
    prefs = get_or_create_preferences(db, demo_user.id)
    prefs.health_alerts = True
    db.add(prefs)
    db.commit()
    return prefs


def auth_header(user_id: int) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id)}"}


def test_password_login_success(client, demo_user):
    resp = client.post(
        "/api/auth/login",
        json={
            "identifier": demo_user.mobile,
            "password": "Demo@1234",
            "remember_me": True,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["access_token"]
    assert body["user"]["mobile"] == demo_user.mobile


def test_password_login_invalid_credentials(client, demo_user):
    resp = client.post(
        "/api/auth/login",
        json={
            "identifier": demo_user.mobile,
            "password": "wrong-password",
            "remember_me": True,
        },
    )
    assert resp.status_code == 401


def test_notification_crud(client, db, demo_user, health_alerts_enabled):
    from pathlib import Path

    from app.models.analysis import Analysis
    from app.models.cow import Cow
    from app.models.detection import Detection

    cow = db.scalar(select(Cow).where(Cow.cow_id == "COW-TEST-001"))
    if not cow:
        db.add(Cow(cow_id="COW-TEST-001", name="COW-TEST-001"))
        db.commit()

    uploads = Path(__file__).resolve().parents[1] / "uploads"
    sample = next(uploads.glob("*.jpg"), None)
    assert sample is not None, "Need at least one file in backend/uploads for notification test."

    analysis = Analysis(
        cow_id="COW-TEST-001",
        image_path=str(sample),
        prediction="Possible mastitis indicators detected",
        confidence=0.87,
        risk_level="Moderate",
        recommendations=["Monitor"],
        model_version="yolo11n",
        demo_mode=False,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(analysis)
    db.flush()
    db.add(
        Detection(
            analysis_id=analysis.id,
            class_name="Mastitis_infected_udder",
            confidence=0.87,
            bbox_x1=10.0,
            bbox_y1=10.0,
            bbox_x2=100.0,
            bbox_y2=100.0,
        )
    )
    db.commit()
    db.refresh(analysis)

    created = create_analysis_notifications(db, analysis, user_id=demo_user.id)
    assert len(created) == 1
    assert created[0].title_key == "notifications.moderateRisk.title"

    headers = auth_header(demo_user.id)
    listed = client.get("/api/notifications", headers=headers)
    assert listed.status_code == 200
    data = listed.json()
    assert data["unread_count"] >= 1
    notif_id = data["notifications"][0]["id"]

    count = client.get("/api/notifications/unread-count", headers=headers)
    assert count.json()["unread_count"] >= 1

    read_one = client.patch(f"/api/notifications/{notif_id}/read", headers=headers)
    assert read_one.status_code == 200
    assert read_one.json()["is_read"] is True

    read_all = client.patch("/api/notifications/read-all", headers=headers)
    assert read_all.status_code == 200


def test_notification_authorization(client, db, demo_user):
    other = db.scalar(select(User).where(User.mobile == "9000000099"))
    if not other:
        other = User(
            full_name="Other",
            mobile="9000000099",
            password_hash=demo_user.password_hash,
            preferred_language="en",
            is_active=True,
        )
        db.add(other)
        db.commit()
        db.refresh(other)

    notif = Notification(
        user_id=demo_user.id,
        type="SYSTEM",
        title_key="notifications.moderateRisk.title",
        message_key="notifications.moderateRisk.message",
        payload={},
        severity="info",
        is_read=False,
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)

    forbidden = client.patch(
        f"/api/notifications/{notif.id}/read",
        headers=auth_header(other.id),
    )
    assert forbidden.status_code == 404


def test_notification_preferences(client, demo_user):
    headers = auth_header(demo_user.id)
    client.put(
        "/api/notifications/preferences",
        headers=headers,
        json={"health_alerts": True, "browser_notifications": False},
    )
    prefs = client.get("/api/notifications/preferences", headers=headers)
    assert prefs.status_code == 200
    assert "health_alerts" in prefs.json()

    updated = client.put(
        "/api/notifications/preferences",
        headers=headers,
        json={"health_alerts": False, "browser_notifications": True},
    )
    assert updated.status_code == 200
    assert updated.json()["health_alerts"] is False


def test_notification_i18n_keys():
    assert "notifications.moderateRisk.title".endswith(".title")
    assert "notifications.moderateRisk.message".endswith(".message")


def test_notification_duplicate_prevention(db, demo_user, health_alerts_enabled):
    from pathlib import Path

    from app.models.analysis import Analysis
    from app.models.cow import Cow

    cow = db.scalar(select(Cow).where(Cow.cow_id == "COW-DUP-001"))
    if not cow:
        db.add(Cow(cow_id="COW-DUP-001", name="COW-DUP-001"))
        db.commit()

    sample = next(Path(__file__).resolve().parents[1].joinpath("uploads").glob("*.jpg"), None)
    assert sample is not None

    analysis = Analysis(
        cow_id="COW-DUP-001",
        image_path=str(sample),
        prediction="Possible mastitis indicators detected",
        confidence=0.87,
        risk_level="Moderate",
        recommendations=["Monitor"],
        model_version="yolo11n",
        demo_mode=False,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    first = create_analysis_notifications(db, analysis, user_id=demo_user.id)
    second = create_analysis_notifications(db, analysis, user_id=demo_user.id)
    assert len(first) == 1
    assert len(second) == 0


def test_mild_risk_notification(db, demo_user, health_alerts_enabled):
    from pathlib import Path

    from app.models.analysis import Analysis
    from app.models.cow import Cow

    cow = db.scalar(select(Cow).where(Cow.cow_id == "COW-MILD-001"))
    if not cow:
        db.add(Cow(cow_id="COW-MILD-001", name="COW-MILD-001"))
        db.commit()

    sample = next(Path(__file__).resolve().parents[1].joinpath("uploads").glob("*.jpg"), None)
    assert sample is not None

    analysis = Analysis(
        cow_id="COW-MILD-001",
        image_path=str(sample),
        prediction="Healthy udder signs detected",
        confidence=0.55,
        risk_level="Mild",
        recommendations=["Monitor"],
        model_version="yolo11n",
        demo_mode=False,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    created = create_analysis_notifications(db, analysis, user_id=demo_user.id)
    assert len(created) == 1
    assert created[0].type == "MILD_RISK"
