"""Login page and authentication logic."""

import reflex as rx
import reflex_chakra as rc

from app.routes import REGISTER_ROUTE
from app.state.login_state import LoginState
from app.state.reset_password_state import ResetPasswordState


def login_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """

    login_form = rc.form(
        rx.fragment(
            rc.flex(
                rc.heading("Log In", as_="h1", size="lg", align="left"),
                padding_bottom="2vh",
            ),
            rc.flex(
                rc.form_label(
                    rc.text(
                        "Email Address",
                        size="md",
                        weight="medium",
                        align="left",
                    ),
                    html_for="email",
                ),
                rc.input(
                    placeholder="email",
                    id="login_email",
                    type_="email",
                ),
                rc.form_label(
                    rc.text(
                        "Password",
                        size="md",
                        weight="bold",
                        align="left",
                    ),
                    html_for="password",
                ),
                rc.password(placeholder="password", id="password"),
                direction="column",
                padding_bottom="2vh",
            ),
            rc.hstack(
                rc.button(
                    "Login",
                    type_="submit",
                    is_loading=LoginState.is_loading,
                    size="lg",
                    variant="outline",
                ),
                rc.button(
                    rx.hstack(
                        rx.icon("github"),
                        rx.text("Login with Github"),
                    ),
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
            rc.vstack(
                rc.flex(
                    rc.heading(
                        "iNotePal", as_="h1", size="4xl", weight="bold", align="left"
                    ),
                    padding_bottom="10vh",
                ),
                rx.cond(  # conditionally show error messages
                    LoginState.error_message != "",
                    rc.alert(
                        rc.alert_icon(),
                        rc.alert_title(LoginState.error_message),
                        status="error",
                    ),
                ),
                login_form,
                rc.link("No account yet? Sign up.", href=REGISTER_ROUTE),
                rc.modal(
                    rc.modal_overlay(
                        rc.modal_content(
                            rc.modal_header("Password Reset"),
                            rc.form(
                                rx.hstack(
                                    rc.input(
                                        placeholder="email",
                                        id="password_reset_email",
                                        type_="email",
                                        width="100%",
                                    ),
                                    rc.box(
                                        width="15px",
                                    ),
                                    rc.button(
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
                                rc.alert(
                                    rc.alert_icon(),
                                    rc.alert_title(ResetPasswordState.error_message),
                                    status="error",
                                ),
                            ),
                            rx.cond(
                                ResetPasswordState.is_requested,
                                rc.alert(
                                    rc.alert_icon(),
                                    rc.alert_title("Password reset mail requested."),
                                    status="success",
                                    border="0.5",
                                ),
                            ),
                            rc.modal_footer(
                                rc.button(
                                    "Close",
                                    on_click=ResetPasswordState.hide_reset_password,
                                )
                            ),
                        )
                    ),
                    is_open=ResetPasswordState.is_show_reset_password,
                ),
                rx.text(
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
                rc.flex(
                    rc.spinner(),
                    height="100vh",
                    weight="100vw",
                    align="center",
                    justify="center",
                ),
            )
        )

    protected_page.__name__ = page.__name__
    return protected_page
