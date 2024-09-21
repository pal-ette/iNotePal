import reflex as rx
from reflex import constants
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class BaseConfg(rx.Config):
    app_name: str = "app"

    backend_port: int = 8080

    api_url: str = f"http://localhost:{backend_port}"


class DevConfig(BaseConfg):
    cors_allowed_origins: List[str] = [
        "http://localhost:3000",
    ]


class ProdConfig(BaseConfg):
    cors_allowed_origins: List[str] = [
        "https://pal-ette.github.io",
    ]

    api_url: str = "https://api.pal-ette.org"

    deploy_url: Optional[str] = "https://pal-ette.github.io/iNotePal"

    frontend_path: str = "/iNotePal"

    db_url = f"postgresql://{os.getenv('POSTGRESQL_USER')}:{os.getenv('POSTGRESQL_PW')}@{os.getenv('POSTGRESQL_HOST')}/postgres"


config = ProdConfig()
env = os.environ.get(constants.ENV_MODE_ENV_VAR)
if env == constants.Env.DEV:
    config = DevConfig()
