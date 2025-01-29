import reflex as rx
import sqlmodel
from typing import Dict, Any


class UserSetting(rx.Model, table=True):
    user_id: str = sqlmodel.Field(
        default=None,
        primary_key=True,
    )

    setting: Dict[str, Any] = sqlmodel.Field(
        default={},
        sa_column=sqlmodel.Column(sqlmodel.JSON, nullable=False),
    )
