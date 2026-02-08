from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Train Tracker API"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+psycopg://postgres:Aicnet%40123@localhost:5432/train_tracker"

    class Config:
        env_file = ".env"

settings = Settings()
