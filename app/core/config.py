# from dotenv import load_dotenv
# import os


# load_dotenv()  # Load environment variables from .env file

class Settings:
    # SECRET: str = os.getenv('SECRET_KEY')
    # ALGO: str = os.getenv('ALGORITHM')
    # ACCESS_EXPIRE: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    # REFRESH_EXPIRE: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES'))

    # Only for Development Work 
    SECRET: str = "your_secret_key"
    ALGO: str = "HS256"
    ACCESS_EXPIRE: int = 1
    REFRESH_EXPIRE: int = 1


settings = Settings()



# Predefined roles and permissions
predefined_roles = [
    {"role_name": "Admin", "permissions": ["read_user", "write_user", "delete_user"]},
    {"role_name": "Editor", "permissions": ["read_user", "write_user"]},
    {"role_name": "Visitor", "permissions": ["read_user"]},
]