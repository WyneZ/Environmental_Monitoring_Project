import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings # type: ignore

load_dotenv()

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB: str = os.getenv("MONGO_DB")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()