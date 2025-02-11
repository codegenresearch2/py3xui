"""This module provides classes to interact with the XUI API."""

from py3xui.api import ClientApi, DatabaseApi, InboundApi
from py3xui.utils import Logger, env

logger = Logger(__name__)


class Api:
    """Class to interact with the XUI API."""

    def __init__(self, host: str, username: str, password: str, skip_login: bool = False):
        """
        Initialize the Api class with the necessary credentials and API clients.

        Args:
            host (str): The API host.
            username (str): The API username.
            password (str): The API password.
            skip_login (bool, optional): Whether to skip the login step. Defaults to False.
        """
        self.client = ClientApi(host, username, password)
        self.inbound = InboundApi(host, username, password)
        self.database = DatabaseApi(host, username, password)
        if not skip_login:
            self.login()

    @classmethod
    def from_env(cls, skip_login: bool = False):
        """
        Create an Api instance from environment variables.

        Args:
            skip_login (bool, optional): Whether to skip the login step. Defaults to False.

        Returns:
            Api: An instance of the Api class.
        """
        host = env.xui_host()
        username = env.xui_username()
        password = env.xui_password()
        return cls(host, username, password, skip_login)

    def login(self) -> None:
        """
        Log in to the API using the provided credentials.

        This method logs in to the API and sets the session for all API clients.
        """
        self.client.login()
        self.inbound.session = self.client.session
        self.database.session = self.client.session
        logger.info("Logged in successfully.")