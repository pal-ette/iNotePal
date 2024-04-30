"""Login page and authentication logic."""

import reflex as rx

from app.routes import REGISTER_ROUTE
from app.state.login_state import LoginState
from app.state.reset_password_state import ResetPasswordState


def login_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """

    login_form = rx.chakra.form(
        rx.fragment(
            rx.chakra.flex(
                rx.chakra.heading("Log In", as_="h1", size="lg", align="left"),
                padding_bottom="2vh",
            ),
            rx.chakra.flex(
                rx.chakra.form_label(
                    rx.chakra.text(
                        "Email Address",
                        size="md",
                        weight="medium",
                        align="left",
                    ),
                    html_for="email",
                ),
                rx.chakra.input(
                    placeholder="email",
                    id="email",
                    type_="email",
                ),
                rx.chakra.form_label(
                    rx.chakra.text(
                        "Password",
                        size="md",
                        weight="bold",
                        align="left",
                    ),
                    html_for="password",
                ),
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
        width="100%",
        on_submit=LoginState.on_submit,
    )

    return rx.fragment(
        rx.cond(
            LoginState.is_hydrated,
            rx.chakra.vstack(
                rx.chakra.flex(
                    rx.chakra.heading(
                        "iNotePal", as_="h1", size="4xl", weight="bold", align="left"
                    ),
                    padding_bottom="10vh",
                ),
                rx.cond(  # conditionally show error messages
                    LoginState.error_message != "",
                    rx.chakra.alert(
                        rx.chakra.alert_icon(),
                        rx.chakra.alert_title(LoginState.error_message),
                        status="error",
                    ),
                ),
                login_form,
                rx.chakra.link("No account yet? Sign up.", href=REGISTER_ROUTE),
                rx.chakra.modal(
                    rx.chakra.modal_overlay(
                        rx.chakra.modal_content(
                            rx.chakra.modal_header("Password Reset"),
                            rx.chakra.form(
                                rx.hstack(
                                    rx.chakra.input(
                                        placeholder="email",
                                        id="email",
                                        type_="email",
                                        width="100%",
                                    ),
                                    rx.chakra.box(
                                        width="15px",
                                    ),
                                    rx.chakra.button(
                                        "Request",
                                        type_="submit",
                                        size="lg",
                                        variant="outline",
                                    ),
                                    margin="0px 20px",
                                    align="center",
                                ),
                                on_submit=ResetPasswordState.request_reset_password,
                            ),
                            rx.cond(
                                ResetPasswordState.error_message != "",
                                rx.chakra.alert(
                                    rx.chakra.alert_icon(),
                                    rx.chakra.alert_title(
                                        ResetPasswordState.error_message
                                    ),
                                    status="error",
                                ),
                            ),
                            rx.cond(
                                ResetPasswordState.is_requested,
                                rx.chakra.alert(
                                    rx.chakra.alert_icon(),
                                    rx.chakra.alert_title(
                                        "Password reset mail requested."
                                    ),
                                    status="success",
                                    border="0.5",
                                ),
                            ),
                            rx.chakra.modal_footer(
                                rx.chakra.button(
                                    "Close",
                                    on_click=ResetPasswordState.hide_reset_password,
                                )
                            ),
                        )
                    ),
                    is_open=ResetPasswordState.is_show_reset_password,
                ),
                rx.chakra.link(
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
                rx.chakra.center(
                    rx.chakra.spinner(),
                ),
            )
        )

    protected_page.__name__ = page.__name__
    return protected_page
