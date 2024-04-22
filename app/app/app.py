"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from dotenv import load_dotenv

from app.app_state import AppState
from app.page.registration import registration_page
from app.page.login import login_page
from app.page.chat import chat
from app.routes import LOGIN_ROUTE, REGISTER_ROUTE

# 외부 정의 DB 모델

load_dotenv()


def show_logout_or_login_comp() -> rx.Component:
    return rx.cond(
        AppState.is_hydrated,
        rx.cond(
            AppState.token_is_valid,
            rx.chakra.box(
                rx.chakra.link("Chat", href="/chat", padding_right="10px"),
                rx.chakra.link("Logout", href="/", on_click=AppState.do_logout),
                spacing="1.5em",
                padding_top="10%",
            ),
            rx.chakra.box(
                rx.chakra.link("Register", href="/register", padding_right="10px"),
                rx.chakra.link("Login", href="/login"),
                spacing="1.5em",
                padding_top="10%",
            ),
        ),
    )


def index() -> rx.Component:
    """Render the index page.

    Returns:
        A reflex component.
    """
    return rx.fragment(
        rx.chakra.color_mode_button(rx.chakra.color_mode_icon(), float="right"),
        rx.chakra.vstack(
            rx.chakra.heading("Welcome to my homepage!", font_size="2em"),
            show_logout_or_login_comp(),
        ),
    )


app = rx.App()
app.add_page(index)
app.add_page(chat, on_load=AppState.check_login)
app.add_page(registration_page, route=REGISTER_ROUTE)
app.add_page(login_page, route=LOGIN_ROUTE)
