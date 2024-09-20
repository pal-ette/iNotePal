import reflex as rx
import sqlmodel
from datetime import date as date_type


class Greeting(rx.Model, table=True):
    date: date_type = sqlmodel.Field(
        default=None,
        primary_key=True,
    )

    message: str
