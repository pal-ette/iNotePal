import reflex as rx
from app.supabase_client import supabase_client
from app.routes import RESET_PASSWORD_ROUTE


class ResetPasswordState(rx.State):
    is_show_reset_password: bool = False

    is_requested: bool = False

    def show_reset_password(self):
        self.is_show_reset_password = True

    def hide_reset_password(self):
        self.is_show_reset_password = False
        self.is_requested = False

    def request_reset_password(self, form_data):
        email = form_data["email"]
        print("Reset password: ", email)
        supabase_client().auth.reset_password_email(
            email,
            {
                "redirect_to": RESET_PASSWORD_ROUTE,
            },
        )
        self.is_requested = True

    def update_password(self, form_data):
        new_password = form_data["password"]
        if new_password is None:
            return
        supabase_client().auth.update_user(
            {
                "password": new_password,
            },
        )
