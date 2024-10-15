import reflex as rx
from app.state.login_state import LoginState
from app.routes import OAUTH_ROUTE


@rx.page(route=OAUTH_ROUTE, on_load=LoginState.on_load_oauth)
def oauth_page() -> rx.Component:
    return rx.flex(
        rx.spinner(),
        height="100vh",
        weight="100vw",
        align="center",
        justify="center",
    )
