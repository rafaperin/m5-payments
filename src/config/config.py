import pathlib
from dotenv import load_dotenv
from pydantic import BaseSettings, validator, PostgresDsn
from typing import Optional, Dict, Any

load_dotenv()

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class PostgresDBSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASS"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str

    ENVIRONMENT: str

    WEBHOOK_BASE_URL: str
    MERCADO_PAGO_ACCESS_TOKEN: str
    MERCADO_PAGO_USER_ID: str
    MERCADO_PAGO_EXTERNAL_POS_ID: str

    ORDERS_SERVICE: str
    PRODUCTS_SERVICE: str

    NEW_ORDER_QUEUE: str
    PAYMENT_CONFIRMATION_TOPIC: str

    db: PostgresDBSettings = PostgresDBSettings()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
