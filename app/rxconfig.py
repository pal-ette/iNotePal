import reflex as rx
from reflex import constants
from reflex.config import environment
import os
from typing import List, Optional
import dotenv

backend_port = 8080
frontend_port = 3000

custom_config = {
    "app_name": "app",
    "backend_port": backend_port,
    "frontend_port": frontend_port,
    "api_url": f"http://localhost:{backend_port}",
    "env_file": ".env",
}

env = environment.REFLEX_ENV_MODE.get()
if env == constants.Env.DEV:
    custom_config["cors_allowed_origins"] = [
        f"http://localhost:{frontend_port}",
    ]
elif env == constants.Env.PROD:
    custom_config["cors_allowed_origins"] = [
        "https://pal-ette.github.io",
    ]
    custom_config["api_url"] = "https://api.pal-ette.org"
    custom_config["deploy_url"] = "https://pal-ette.github.io/iNotePal"
    custom_config["frontend_path"] = "/iNotePal"
    custom_config["db_url"] = (
        f"postgresql://{os.getenv('POSTGRESQL_USER')}:{os.getenv('POSTGRESQL_PW')}@{os.getenv('POSTGRESQL_HOST')}/postgres"
    )

config = rx.Config(**custom_config)
