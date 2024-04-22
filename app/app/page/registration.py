"""New user registration form and validation logic."""

from __future__ import annotations

import reflex as rx

from app.routes import REGISTER_ROUTE
from app.state.registration_state import RegistrationState


def registration_page() -> rx.Component:
    """Render the registration page.

    Returns:
        A reflex component.
    """
    register_form = rx.chakra.form(
        rx.chakra.input(placeholder="email", id="email", type_="email"),
        rx.chakra.password(placeholder="password", id="password"),
        rx.chakra.password(placeholder="confirm", id="confirm_password"),
        rx.chakra.button(
            "Register",
            type_="submit",
            is_loading=RegistrationState.is_loading,
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
                padding_top="10vh",
            ),
        )
    )
