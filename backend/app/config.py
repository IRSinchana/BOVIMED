"""Central configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_ROOT.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            str(PROJECT_ROOT / ".env"),
            str(BACKEND_ROOT / ".env"),
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    demo_mode: bool = Field(default=False, alias="DEMO_MODE")
    model_path: str = Field(default="models/best.pt", alias="MODEL_PATH")
    database_url: str = Field(
        default=f"sqlite:///{(BACKEND_ROOT / 'bovimed.db').as_posix()}",
        alias="DATABASE_URL",
    )
    max_upload_size_mb: int = Field(default=10, alias="MAX_UPLOAD_SIZE_MB")
    cors_origins: str = Field(
        default=(
            "http://localhost:5173,http://127.0.0.1:5173,"
            "http://localhost:5174,http://127.0.0.1:5174,"
            "https://bovimed.vercel.app"
        ),
        alias="CORS_ORIGINS",
    )

    healthy_threshold: float = Field(default=0.30, alias="HEALTHY_THRESHOLD")
    mild_threshold: float = Field(default=0.55, alias="MILD_THRESHOLD")
    moderate_threshold: float = Field(default=0.75, alias="MODERATE_THRESHOLD")
    severe_threshold: float = Field(default=0.90, alias="SEVERE_THRESHOLD")

    jwt_secret: str = Field(
        default="bovimed-dev-secret-change-in-production",
        alias="JWT_SECRET",
    )
    google_places_api_key: str | None = Field(default=None, alias="GOOGLE_PLACES_API_KEY")
    vet_provider: str | None = Field(default=None, alias="VET_PROVIDER")

    bovimed_llm_enabled: bool = Field(default=False, alias="BOVIMED_LLM_ENABLED")
    bovimed_llm_provider: str | None = Field(default=None, alias="BOVIMED_LLM_PROVIDER")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    bovimed_llm_api_key: str | None = Field(default=None, alias="BOVIMED_LLM_API_KEY")
    gemini_model: str = Field(default="gemini-1.5-flash", alias="GEMINI_MODEL")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    model_version: str = Field(default="yolo11-bovimed-v1", alias="MODEL_VERSION")
    max_image_dimension: int = Field(default=1280, alias="MAX_IMAGE_DIMENSION")

    otp_provider: str | None = Field(default=None, alias="OTP_PROVIDER")
    otp_api_key: str | None = Field(default=None, alias="OTP_API_KEY")
    otp_sender_id: str | None = Field(default=None, alias="OTP_SENDER_ID")
    otp_template_id: str | None = Field(default=None, alias="OTP_TEMPLATE_ID")
    otp_twilio_account_sid: str | None = Field(default=None, alias="OTP_TWILIO_ACCOUNT_SID")
    otp_twilio_auth_token: str | None = Field(default=None, alias="OTP_TWILIO_AUTH_TOKEN")
    otp_dev_mode: bool = Field(default=False, alias="OTP_DEV_MODE")

    smtp_host: str | None = Field(default=None, alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_username: str | None = Field(default=None, alias="SMTP_USERNAME")
    smtp_password: str | None = Field(default=None, alias="SMTP_PASSWORD")
    smtp_from: str | None = Field(default=None, alias="SMTP_FROM")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def resolved_model_path(self) -> Path:
        """Resolve model path relative to the backend project (not a hard-coded OS path)."""
        path = Path(self.model_path)
        if path.is_absolute():
            return path

        candidates = [
            BACKEND_ROOT / path,  # models/best.pt when cwd/config is backend-relative
            PROJECT_ROOT / path,  # backend/models/best.pt from repo root .env
            BACKEND_ROOT / "models" / "best.pt",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return candidate.resolve()
        # Prefer canonical backend-relative location even if missing
        return (BACKEND_ROOT / "models" / "best.pt").resolve()

    @property
    def uploads_dir(self) -> Path:
        path = BACKEND_ROOT / "uploads"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def results_dir(self) -> Path:
        path = BACKEND_ROOT / "results"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    def should_use_demo_mode(self) -> bool:
        """Demo only when explicitly enabled. Real mode requires best.pt."""
        return bool(self.demo_mode)


@lru_cache
def get_settings() -> Settings:
    return Settings()


def clear_settings_cache() -> None:
    get_settings.cache_clear()
