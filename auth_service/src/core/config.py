import os
from logging import config as logging_config

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class AuthJWT(BaseModel):
    secret_key: str = "secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 20 * 60
    refresh_token_expire_minutes: int = 30 * 24 * 60 * 60  # 30 дней


class YandexSettings(BaseSettings):
    oauth_url: str = "https://oauth.yandex.ru/"
    login_url: str = "https://login.yandex.ru/"
    client_id: str = "test"
    client_secret: str = "test"

    class Config:
        env_file = "providers.env"


class Settings(BaseSettings):
    project_name: str

    service_port: int
    service_host: str

    # Настройки postgres
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    # Настройки Redis
    redis_host: str
    redis_port: int

    # Настройки jwt
    auth_jwt: AuthJWT = AuthJWT()
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    REQUEST_LIMIT_PER_MINUTE: int = os.getenv("REQUEST_LIMIT_PER_MINUTE", 20)

    # Настройка трассировки
    tracer_host: str
    tracer_port: int
    enable_tracer: bool

    class Config:
        env_file = ".env"


settings = Settings()
yandex_settings = YandexSettings()
page_max_size = 100
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PostgreSQLConfig(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int


pg_config_data = PostgreSQLConfig(
    dbname=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
)
