from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Email
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
