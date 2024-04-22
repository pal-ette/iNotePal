"""Login page and authentication logic."""

import reflex as rx

from app.routes import REGISTER_ROUTE
from app.state.login_state import LoginState


def login_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """
    login_form = rx.chakra.form(
        rx.chakra.input(placeholder="email", id="email", type_="email"),
        rx.chakra.password(placeholder="password", id="password"),
        rx.chakra.button("Login", type_="submit", is_loading=LoginState.is_loading),
        width="80vw",
        on_submit=LoginState.on_submit,
    )

    return rx.fragment(
        rx.cond(
            LoginState.is_hydrated,
            rx.chakra.vstack(
                rx.cond(  # conditionally show error messages
                    LoginState.error_message != "",
                    rx.chakra.text(LoginState.error_message),
                ),
                login_form,
                rx.chakra.link("Register", href=REGISTER_ROUTE),
                padding_top="10vh",
            ),
        )
    )


def require_login(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated. do not rendering anything.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """

    def protected_page():
        return rx.fragment(
            rx.cond(
                LoginState.is_hydrated,
                rx.cond(
                    LoginState.token_is_valid,
                    page(),
                ),
                rx.chakra.center(
                    rx.chakra.spinner(),
                ),
            )
        )

    protected_page.__name__ = page.__name__
    return protected_page
