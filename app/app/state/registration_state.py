import reflex as rx
import asyncio
import re
from collections.abc import AsyncGenerator
from app.app_state import AppState
from app.routes import LOGIN_ROUTE
from app.supabase_client import supabase_client


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


class RegistrationState(AppState):
    """Handle registration form submission and redirect to login page after registration."""

    success: bool = False
    error_message: str = ""

    is_loading: bool = False

    async def handle_registration(
        self, form_data
    ) -> AsyncGenerator[rx.event.EventSpec | list[rx.event.EventSpec] | None, None]:
        """Handle registration form on_submit.

        Set error_message appropriately based on validation results.

        Args:
            form_data: A dict of form fields and values.
        """

        # set the following values to spin the button
        self.is_loading = True
        yield

        email = form_data["email"]
        if not email:
            self.error_message = "email cannot be empty"
            rx.set_focus("email")
            # reset state variable again
            self.is_loading = False
            yield
            return
        if not is_valid_email(email):
            self.error_message = "email is not a valid email address."
            rx.set_focus("email")
            # reset state variable again
            self.is_loading = False
            yield
            return

        password = form_data["password"]
        if not password:
            self.error_message = "Password cannot be empty"
            rx.set_focus("password")
            # reset state variable again
            self.is_loading = False
            yield
            return
        if password != form_data["confirm_password"]:
            self.error_message = "Passwords do not match"
            [
                rx.set_value("confirm_password", ""),
                rx.set_focus("confirm_password"),
            ]
            # reset state variable again
            self.is_loading = False
            yield
            return

        # sign up with supabase
        supabase_client().auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

        # Set success and redirect to login page after a brief delay.
        self.error_message = ""
        self.success = True
        self.is_loading = False
        yield
        await asyncio.sleep(3)
        yield [rx.redirect(LOGIN_ROUTE), RegistrationState.set_success(False)]
