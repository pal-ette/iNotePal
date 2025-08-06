"""
Top-level State for the App.

Authentication data is stored in the base State class so that all substates can
access it for verifying access to event handlers and computed vars.
"""

import os
import jwt
import time
import reflex as rx
import reflex_local_auth

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


class AppState(reflex_local_auth.LocalAuthState):
    def on_load(self):
        if not self.is_authenticated:
            return reflex_local_auth.LoginState.redir

    def do_logout(self):
        self.data = ""
        return reflex_local_auth.LocalAuthState.do_logout
