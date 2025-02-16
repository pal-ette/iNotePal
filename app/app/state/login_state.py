import reflex as rx
import asyncio

from app.app_state import AppState
from app.supabase_client import supabase_client
from app.routes import LOGIN_ROUTE, OAUTH_ROUTE, DASHBOARD_ROUTE
from reflex.config import get_config


class LoginState(AppState):
    """Handle login form submission and redirect to proper routes after authentication."""

    error_message: str = ""
    redirect_to: str = ""

    is_loading: bool = False

    def on_load_oauth(self):
        sharp_param = f"{OAUTH_ROUTE}/#"
        if self.router.page.raw_path.startswith(sharp_param):
            return rx.redirect(
                self.router.page.raw_path.replace(sharp_param, f"{OAUTH_ROUTE}/?")
            )

        try:
            auth_response = supabase_client().auth.set_session(
                access_token=self.router.page.params["access_token"],
                refresh_token=self.router.page.params["refresh_token"],
            )
            self.auth_token = auth_response.session.access_token
            self.error_message = ""
            self.redirect_to = ""
        except Exception as e:
            print("oauth error:", str(e))

        return LoginState.redir()

    def login_with_github(self):
        self.is_loading = True
        yield
        redirect_to = (
            f"{self.router.page.host}{get_config().frontend_path}{OAUTH_ROUTE}"
        )
        data = supabase_client().auth.sign_in_with_oauth(
            {
                "provider": "github",
                "options": {"redirect_to": redirect_to},
            }
        )
        self.redirect_to = data.url
        return LoginState.redir()

    def on_submit(self, form_data):
        """Handle login form on_submit.

        Args:
            form_data: A dict of form fields and values.
        """

        # set the following values to spin the button
        self.is_loading = True
        yield

        self.error_message = ""
        email = form_data["login_email"]
        password = form_data["password"]

        try:
            auth_response = supabase_client().auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                },
            )
            self.auth_token = auth_response.session.access_token
            self.error_message = ""
            self.redirect_to = ""
            return LoginState.redir()
        except:
            self.error_message = "There was a problem logging in, please try again."

            # reset state variable again
            self.is_loading = False

    async def redir(self):
        """Redirect to the redirect_to route if logged in, or to the login page if not."""
        if not self.is_hydrated:
            # wait until after hydration
            return LoginState.redir()
        page = self.router.page.path

        await asyncio.sleep(2)
        if not self.token_is_valid and page != LOGIN_ROUTE:
            self.redirect_to = page

            # reset state variable again
            self.is_loading = False

            return rx.redirect(LOGIN_ROUTE)
        else:
            # reset state variable again
            self.is_loading = False

            return rx.redirect(self.redirect_to or DASHBOARD_ROUTE)
