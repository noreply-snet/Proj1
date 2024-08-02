from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings:
    SECRET: str = os.getenv('SECRET_KEY')
    ALGO: str = os.getenv('ALGORITHM')
    ACCESS_EXPIRE: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    REFRESH_EXPIRE: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES'))

settings = Settings()
