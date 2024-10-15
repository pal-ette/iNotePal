"""Reset password of user"""

import reflex as rx
from app.routes import RESET_PASSWORD_ROUTE


@rx.page(route=RESET_PASSWORD_ROUTE)
def reset_password_page() -> rx.Component:

    return rx.text("")
