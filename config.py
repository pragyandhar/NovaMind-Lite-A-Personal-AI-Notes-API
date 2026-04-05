from pydantic_settings import BaseSettings
from pydantic import ConfigDict
# -----------------------------------------

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    # Environment Variables Define
    jwt_secret_key: str
    groq_api_key: str
    database_url: str = "sqlite:///./novamind.db"
    access_token_expire_minutes: int = 30

    # class Config:
    #     env_file = ".env"

    # Production-level structuring
    environment: str = "development"
    debug: bool = True    

settings = Settings()
