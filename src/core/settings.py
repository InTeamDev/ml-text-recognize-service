from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'ml-recognize-service'
    BASE_URL: str = '/api'

    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str

    def get_dsn(self):
        return f'mongodb://{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}'


load_dotenv()
settings = Settings()  # type: ignore
