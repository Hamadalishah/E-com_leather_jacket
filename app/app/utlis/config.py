# app/config.py
from pydantic_settings import BaseSettings # type: ignore
from pydantic import Field

class Settings(BaseSettings): 
    SUPABASE_ENDPOINT: str
    SUPABASE_BUCKET_NAME: str
    SUPABASE_SERVICE_ROLE_TOKEN: str
    DATABASE_URL: str
    TIMEOUT_SECONDS: int = Field(default=10)

    class Config:
        env_file = ".env"

settings = Settings()
