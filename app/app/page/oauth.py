import reflex as rx
import reflex_chakra as rc
from app.supabase_client import supabase_client


def oauth_page() -> rx.Component:
    return rc.flex(
        rc.spinner(),
        height="100vh",
        weight="100vw",
        align="center",
        justify="center",
    )
