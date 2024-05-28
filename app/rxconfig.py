import reflex as rx
from reflex import constants
import os
from typing import List, Optional


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

    api_url: str = "https://nvidia.edens.one"

    deploy_url: Optional[str] = "https://pal-ette.github.io/iNotePal"

    frontend_path: str = "/iNotePal"


config = ProdConfig()
env = os.environ.get(constants.ENV_MODE_ENV_VAR)
if env == constants.Env.DEV:
    config = DevConfig()
