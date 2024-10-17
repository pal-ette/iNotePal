"""Login page and authentication logic."""

import reflex as rx

from app.state.login_state import LoginState
from app.state.reset_password_state import ResetPasswordState
from app.routes import LOGIN_ROUTE, REGISTER_ROUTE


@rx.page(route=LOGIN_ROUTE)
def login_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """

    login_form = rx.form(
        rx.fragment(
            rx.flex(
                rx.heading("Log In", as_="h1", size="lg", align="left"),
                padding_bottom="2vh",
            ),
            rx.flex(
                rx.text(
                    "Email Address",
                    size="md",
                    weight="medium",
                    align="left",
                ),
                rx.input(
                    placeholder="email",
                    id="login_email",
                    type_="email",
                ),
                rx.text(
                    "Password",
                    size="md",
                    weight="bold",
                    align="left",
                ),
                rx.input(placeholder="password", id="password", type="password"),
                direction="column",
                padding_bottom="2vh",
            ),
            rx.hstack(
                rx.button(
                    "Login",
                    type_="submit",
                    loading=LoginState.is_loading,
                    size="lg",
                    variant="outline",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("github"),
                        rx.text("Login with Github"),
                    ),
                    type="button",
                    loading=LoginState.is_loading,
                    on_click=LoginState.login_with_github,
                ),
            ),
        ),
        width="100%",
        on_submit=LoginState.on_submit,
    )

    return rx.fragment(
        rx.cond(
            LoginState.is_hydrated,
            rx.vstack(
                rx.flex(
                    rx.heading(
                        "iNotePal", as_="h1", size="4xl", weight="bold", align="left"
                    ),
                    padding_bottom="10vh",
                ),
                rx.cond(  # conditionally show error messages
                    LoginState.error_message != "",
                    rx.callout(
                        LoginState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),
                login_form,
                rx.link("No account yet? Sign up.", href=REGISTER_ROUTE),
                rx.dialog.root(
                    rx.dialog.content(
                        rx.heading("Password Reset"),
                        rx.form(
                            rx.hstack(
                                rx.input(
                                    placeholder="email",
                                    id="password_reset_email",
                                    type_="email",
                                    width="100%",
                                ),
                                rx.box(
                                    width="15px",
                                ),
                                rx.button(
                                    "Request",
                                    type_="submit",
                                    size="lg",
                                    variant="outline",
                                ),
                                rx.button(
                                    "Close",
                                    type="button",
                                    on_click=ResetPasswordState.hide_reset_password,
                                ),
                                margin="0px 20px",
                                align="center",
                            ),
                            on_submit=ResetPasswordState.request_reset_password,
                        ),
                        rx.cond(
                            ResetPasswordState.error_message != "",
                            rx.callout(
                                ResetPasswordState.error_message,
                                icon="triangle_alert",
                                color_scheme="red",
                                role="alert",
                            ),
                        ),
                        rx.cond(
                            ResetPasswordState.is_requested,
                            rx.callout(
                                "Password reset mail requested.",
                                icon="info",
                                color_scheme="green",
                            ),
                        ),
                    ),
                    open=ResetPasswordState.is_show_reset_password,
                ),
                rx.link(
                    "Forgot password?",
                    on_click=ResetPasswordState.show_reset_password,
                ),
                padding_top="3vh",
                margin="0px 10vw",
                align="center",
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
                rx.flex(
                    rx.spinner(),
                    height="100vh",
                    weight="100vw",
                    align="center",
                    justify="center",
                ),
            )
        )

    protected_page.__name__ = page.__name__
    return protected_page
