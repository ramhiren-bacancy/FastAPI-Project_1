from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    # model_config = SettingsConfigDict(env_file="../../.env",extra="ignore")
    # DB_CONNECTION: str = "postgresql://postgres:root@localhost:5432/fastapi_Todo" # ! Sync DATABASE
    # DB_CONNECTION: str = "postgresql+asyncpg://postgres:root@localhost:5432/fastapi_Todo" # ! Async DATABASE
    # SECRET_KEY:str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    # ALGORITHM:str = "HS256"
    # EXP_TIME:int =30
    DB_CONNECTION: str
    SECRET_KEY:str
    ALGORITHM:str
    EXP_TIME:int
    

settings = Settings()

print(settings.DB_CONNECTION)