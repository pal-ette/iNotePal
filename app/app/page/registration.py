"""New user registration form and validation logic."""

from __future__ import annotations

import reflex as rx

from app.routes import REGISTER_ROUTE, LOGIN_ROUTE
from app.state.registration_state import RegistrationState


def registration_page() -> rx.Component:
    """Render the registration page.

    Returns:
        A reflex component.
    """
    register_form = rx.chakra.form(
        rx.fragment(
            rx.chakra.flex(
                rx.chakra.heading(
                    "iNotePal", as_="h1", size="4xl", weight="bold", align="left"
                ),
                padding_bottom="10vh",
            ),
            rx.chakra.flex(
                rx.chakra.heading("Sign up", as_="h1", size="lg", align="left"),
                padding_bottom="2vh",
            ),
            rx.chakra.flex(
                rx.chakra.text(
                    "Email Address", size="md", weight="medium", align="left"
                ),
                rx.chakra.input(placeholder="email", id="email", type_="email"),
                rx.chakra.text("Password", size="md", weight="bold", align="left"),
                rx.chakra.password(placeholder="password", id="password"),
                rx.chakra.text(
                    "Confirm Password", size="md", weight="bold", align="left"
                ),
                rx.chakra.password(
                    placeholder="confirm password", id="confirm_password"
                ),
                direction="column",
                padding_bottom="2vh",
            ),
            rx.chakra.flex(
                rx.chakra.button(
                    "Register",
                    type_="submit",
                    is_loading=RegistrationState.is_loading,
                    size="lg",
                    variant="outline",
                )
            ),
        ),
        width="80vw",
        on_submit=RegistrationState.handle_registration,
    )

    return rx.fragment(
        rx.cond(
            RegistrationState.success,
            rx.chakra.vstack(
                rx.chakra.text(
                    "Registration successful, check your mail to confirm signup so as to login!"
                ),
                rx.chakra.spinner(),
            ),
            rx.chakra.vstack(
                rx.cond(  # conditionally show error messages
                    RegistrationState.error_message != "",
                    rx.chakra.text(RegistrationState.error_message),
                ),
                register_form,
                rx.chakra.link("Already have an account?", href=LOGIN_ROUTE),
            ),
        ),
    )
