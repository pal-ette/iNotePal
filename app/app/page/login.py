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
        rx.fragment(
            rx.chakra.flex(
                rx.chakra.heading(
                    "iNotePal", as_="h1", size="4xl", weight="bold", align="left"
                ),
                padding_bottom="10vh",
            ),
            rx.chakra.flex(
                rx.chakra.heading("Log In", as_="h1", size="lg", align="left"),
                padding_bottom="2vh",
            ),
            rx.chakra.flex(
                rx.chakra.text(
                    "Email Address", size="md", weight="medium", align="left"
                ),
                rx.chakra.input(placeholder="email", id="email", type_="email"),
                rx.chakra.text("Password", size="md", weight="bold", align="left"),
                rx.chakra.password(placeholder="password", id="password"),
                direction="column",
                padding_bottom="2vh",
            ),
            rx.chakra.flex(
                rx.chakra.button(
                    "Login",
                    type_="submit",
                    is_loading=LoginState.is_loading,
                    size="lg",
                    variant="outline",
                )
            ),
        ),
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
                rx.chakra.link("No account yet? Sign up.", href=REGISTER_ROUTE),
                padding_top="3vh",
            ),
        ),
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
