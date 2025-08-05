"""Login page and authentication logic."""

import reflex as rx

from app.state.login_state import LoginState
from app.routes import LOGIN_ROUTE, REGISTER_ROUTE
from app.component.logo import logo


@rx.page(
    route=LOGIN_ROUTE,
    on_load=LoginState.check_not_login,
)
def login_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """

    login_form = rx.form(
        rx.fragment(
            rx.flex(
                rx.heading(
                    "로그인",
                    as_="h1",
                    size="6",
                    align="left",
                ),
                padding_bottom="2vh",
            ),
            rx.flex(
                rx.text(
                    "이메일",
                    size="3",
                    weight="medium",
                    align="left",
                ),
                rx.input(
                    placeholder="이메일",
                    id="login_email",
                    type_="email",
                ),
                rx.text(
                    "비밀번호",
                    size="3",
                    weight="bold",
                    align="left",
                ),
                rx.input(
                    placeholder="비밀번호",
                    id="password",
                    type="password",
                ),
                direction="column",
                padding_bottom="2vh",
            ),
            rx.hstack(
                rx.button(
                    "로그인",
                    type_="submit",
                    loading=LoginState.is_loading,
                    variant="outline",
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
                    logo(size="7"),
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
                rx.link("아직 계정이 없으신가요? 가입하러 가기", href=REGISTER_ROUTE),
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
