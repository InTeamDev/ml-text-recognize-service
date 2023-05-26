from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'ml-recognize-service'
    BASE_URL: str = '/api'

    MONGO_DSN: str


load_dotenv()
settings = Settings()  # type: ignore
