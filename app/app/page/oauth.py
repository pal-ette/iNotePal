import reflex as rx
from app.supabase_client import supabase_client


def oauth_page() -> rx.Component:
    return rx.chakra.flex(
        rx.chakra.spinner(),
        height="100vh",
        weight="100vw",
        align="center",
        justify="center",
    )
