from functools import lru_cache

from pydantic import SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/gp_autos"
    frontend_url: str = "http://localhost:3000"
    environment: str = "development"
    session_secret: SecretStr = SecretStr("local-development-secret-change-before-deploy")
    session_cookie_name: str = "gp_autos_session"
    session_max_age_seconds: int = 60 * 60 * 24 * 7
    google_client_id: str = ""
    google_client_secret: SecretStr = SecretStr("")
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"
    paystack_secret_key: SecretStr = SecretStr("")
    paystack_public_key: str = ""
    paystack_callback_url: str = ""
    paystack_base_url: str = "https://api.paystack.co"
    mailgun_api_key: SecretStr = SecretStr("")
    mailgun_domain: str = ""
    mailgun_from_email: str = "GP Autos <orders@gpautos.example>"
    mailgun_base_url: str = "https://api.mailgun.net"

    @field_validator("paystack_callback_url", mode="after")
    @classmethod
    def default_paystack_callback_url(cls, value: str, info: ValidationInfo) -> str:
        if value:
            return value.rstrip("/")
        environment = str(info.data.get("environment") or "").lower()
        frontend_url = (info.data.get("frontend_url") or "").strip()
        if not frontend_url:
            frontend_url = (
                "https://gp-autos.vercel.app"
                if environment == "production"
                else "http://localhost:3000"
            )
        elif environment == "production" and frontend_url == "http://localhost:3000":
            frontend_url = "https://gp-autos.vercel.app"
        return f"{frontend_url.rstrip('/')}/orders/confirmation"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
