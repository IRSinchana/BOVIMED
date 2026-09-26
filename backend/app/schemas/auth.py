from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=128)
    mobile: str = Field(..., min_length=10, max_length=15)
    email: str | None = Field(default=None, max_length=255)
    password: str = Field(..., min_length=6, max_length=72)
    confirm_password: str = Field(..., min_length=6, max_length=72)
    farm_name: str | None = Field(default=None, max_length=128)
    state: str | None = Field(default=None, max_length=64)
    district: str | None = Field(default=None, max_length=64)

    @field_validator("mobile")
    @classmethod
    def normalize_mobile(cls, v: str) -> str:
        digits = "".join(ch for ch in v if ch.isdigit())
        if len(digits) < 10:
            raise ValueError("Enter a valid mobile number.")
        return digits[-10:] if len(digits) >= 10 else digits

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str | None) -> str | None:
        if v is None or not str(v).strip():
            return None
        return str(v).strip().lower()


class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=255, description="Mobile or email")
    password: str = Field(..., min_length=1, max_length=72)
    remember_me: bool = False


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=128)
    farm_name: str | None = Field(default=None, max_length=128)
    state: str | None = Field(default=None, max_length=64)
    district: str | None = Field(default=None, max_length=64)
    preferred_language: str | None = Field(default=None, max_length=16)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    mobile: str
    email: str | None = None
    farm_name: str | None = None
    state: str | None = None
    district: str | None = None
    preferred_language: str
    created_at: datetime


class AuthResponse(BaseModel):
    success: bool = True
    access_token: str
    token_type: str = "bearer"
    user: UserOut
