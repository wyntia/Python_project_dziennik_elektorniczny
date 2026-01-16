from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any

class Settings(BaseSettings):
    """
    Klasa przechowująca konfigurację aplikacji ładowaną z pliku .env.
    """
    PROJECT_NAME: str = "School Gradebook"
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()