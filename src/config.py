from pathlib import Path
from dotenv import load_dotenv
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent

if load_dotenv():
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PATH = f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    
class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_PATH}"
    echo: bool = False # True - for debug

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    email_validation_api_url: str = "https://emailvalidation.abstractapi.com/v1/"
    email_validation_api_key: str = "971de29514094d948e2f633a3b47392e"
    db: DbSettings = DbSettings()
    auth: AuthJWT = AuthJWT()

settings = Settings()