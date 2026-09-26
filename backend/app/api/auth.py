"""Authentication and farmer profile endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    UserOut,
)
from app.services.auth_service import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


def _user_out(user: User) -> UserOut:
    return UserOut.model_validate(user)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password do not match.",
        )

    existing_mobile = db.scalar(select(User).where(User.mobile == payload.mobile))
    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this mobile number already exists.",
        )

    if payload.email:
        email_taken = db.scalar(select(User).where(User.email == payload.email))
        if email_taken:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

    user = User(
        full_name=payload.full_name.strip(),
        mobile=payload.mobile,
        email=payload.email,
        password_hash=hash_password(payload.password),
        farm_name=(payload.farm_name or "").strip() or None,
        state=(payload.state or "").strip() or None,
        district=(payload.district or "").strip() or None,
        preferred_language="en",
        is_active=True,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create account. Please try again.",
        ) from exc

    token = create_access_token(user.id)
    return AuthResponse(access_token=token, user=_user_out(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    ident = payload.identifier.strip()
    digits = "".join(ch for ch in ident if ch.isdigit())
    user = None
    if "@" in ident:
        user = db.scalar(select(User).where(User.email == ident.lower()))
    else:
        mobile = digits[-10:] if len(digits) >= 10 else digits
        user = db.scalar(select(User).where(User.mobile == mobile))

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect mobile/email or password.",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive.",
        )

    token = create_access_token(user.id)
    return AuthResponse(access_token=token, user=_user_out(user))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return _user_out(current_user)


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    # JWT is stateless; client discards the token. Endpoint confirms session end.
    return {
        "success": True,
        "message": "Logged out successfully.",
        "user_id": current_user.id,
    }


@router.put("/profile", response_model=UserOut)
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        if value is not None:
            setattr(current_user, key, value.strip() if isinstance(value, str) else value)
    try:
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save profile.",
        ) from exc
    return _user_out(current_user)
