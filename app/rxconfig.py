import reflex as rx
from reflex import constants
from reflex.config import environment
import os
from typing import List, Optional
import dotenv

backend_port = 8080
frontend_port = 3000


class BaseConfg(rx.Config):
    app_name: str = "app"

    backend_port: int = backend_port

    frontend_port: int = frontend_port

    api_url: str = f"http://localhost:{backend_port}"

    env_file: Optional[str] = ".env"


class DevConfig(BaseConfg):
    cors_allowed_origins: List[str] = [
        f"http://localhost:{frontend_port}",
    ]


class ProdConfig(BaseConfg):
    cors_allowed_origins: List[str] = [
        "https://pal-ette.github.io",
    ]

    api_url: str = "https://api.pal-ette.org"

    deploy_url: Optional[str] = "https://pal-ette.github.io/iNotePal"

    frontend_path: str = "/iNotePal"

    db_url = f"postgresql://{os.getenv('POSTGRESQL_USER')}:{os.getenv('POSTGRESQL_PW')}@{os.getenv('POSTGRESQL_HOST')}/postgres"


config = BaseConfg()
env = environment.REFLEX_ENV_MODE.get()
if env == constants.Env.DEV:
    config = DevConfig()
elif env == constants.Env.PROD:
    config = ProdConfig()
