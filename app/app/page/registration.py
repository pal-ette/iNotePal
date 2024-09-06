"""New user registration form and validation logic."""

from __future__ import annotations

import reflex as rx
import reflex_chakra as rc

from app.routes import REGISTER_ROUTE, LOGIN_ROUTE
from app.state.registration_state import RegistrationState


def registration_page() -> rx.Component:
    """Render the registration page.

    Returns:
        A reflex component.
    """
    register_form = rc.form(
        rx.fragment(
            rc.flex(
                rc.heading(
                    "iNotePal", as_="h1", size="4xl", weight="bold", align="left"
                ),
                padding_bottom="10vh",
            ),
            rc.flex(
                rc.heading("Sign up", as_="h1", size="lg", align="left"),
                padding_bottom="2vh",
            ),
            rc.flex(
                rc.text("Email Address", size="md", weight="medium", align="left"),
                rc.input(placeholder="email", id="email", type_="email"),
                rc.text("Password", size="md", weight="bold", align="left"),
                rc.password(placeholder="password", id="password"),
                rc.text("Confirm Password", size="md", weight="bold", align="left"),
                rc.password(placeholder="confirm password", id="confirm_password"),
                direction="column",
                padding_bottom="2vh",
            ),
            rc.flex(
                rc.button(
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
            rc.vstack(
                rc.text(
                    "Registration successful, check your mail to confirm signup so as to login!"
                ),
                rc.spinner(),
            ),
            rc.vstack(
                rx.cond(  # conditionally show error messages
                    RegistrationState.error_message != "",
                    rc.text(RegistrationState.error_message),
                ),
                register_form,
                rc.link("Already have an account?", href=LOGIN_ROUTE),
            ),
        ),
    )
