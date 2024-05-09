import reflex as rx
from app.supabase_client import supabase_client
from app.routes import RESET_PASSWORD_ROUTE


class ResetPasswordState(rx.State):
    is_show_reset_password: bool = False

    is_requested: bool = False

    error_message: str = ""

    def show_reset_password(self):
        self.is_show_reset_password = True

    def hide_reset_password(self):
        self.is_show_reset_password = False
        self.is_requested = False
        self.error_message = ""

    def request_reset_password(self, form_data):
        self.error_message = ""
        email = form_data["password_reset_email"]
        try:
            supabase_client().auth.reset_password_email(
                email,
                {
                    "redirect_to": RESET_PASSWORD_ROUTE,
                },
            )
            self.is_requested = True
        except Exception as e:
            self.error_message = str(e)

    def update_password(self, form_data):
        self.error_message = ""
        new_password = form_data["password"]
        if new_password is None:
            return
        try:
            supabase_client().auth.update_user(
                {
                    "password": new_password,
                },
            )
        except Exception as e:
            self.error_message = str(e)
