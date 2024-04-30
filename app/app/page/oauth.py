import reflex as rx
from app.supabase_client import supabase_client


def oauth_page() -> rx.Component:
    return rx.text("?")
