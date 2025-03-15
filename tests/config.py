from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс конфигурируемые параметры приложения. Параметры могут быть переопределены
    в файле .env в корне проекта или через переменные окружения."""

    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_USER: str = "demo"
    DB_PASSWORD: str = "demo"
    DB_NAME: str = "demo"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
