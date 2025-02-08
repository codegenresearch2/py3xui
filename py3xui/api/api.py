from __future__ import annotations

"""This module provides classes to interact with the XUI API."""

from py3xui.api import ClientApi, DatabaseApi, InboundApi
from py3xui.utils import Logger, env

logger = Logger(__name__)


class Api:
    """Class to interact with the XUI API."

    def __init__(self, host: str, username: str, password: str, skip_login: bool = False):
        """Initialize the API client."
        self.host = host
        self.username = username
        self.password = password
        self.skip_login = skip_login
        self.client = ClientApi(host, username, password)
        self.inbound = InboundApi(host, username, password)
        self.database = DatabaseApi(host, username, password)
        if not skip_login:
            self.login()

    @classmethod
    def from_env(cls, skip_login: bool = False) -> Api:
        """Initialize the API client from environment variables."
        host = env.xui_host()
        username = env.xui_username()
        password = env.xui_password()
        return cls(host, username, password, skip_login)

    def login(self) -> None:
        """Log in to the API."
        self.client.login()
        self.inbound.session = self.client.session
        self.database.session = self.client.session
        logger.info("Logged in successfully.")
