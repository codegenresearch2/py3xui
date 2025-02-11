"""This module provides classes to interact with the XUI API."""

from __future__ import annotations
from py3xui.api import ClientApi, DatabaseApi, InboundApi
from py3xui.utils import Logger, env

logger = Logger(__name__)


class Api:
    """A high-level interface to interact with the XUI API.

    This class provides methods to interact with the XUI API using the provided credentials.
    It handles the login process automatically if not skipped.

    Attributes:
        host (str): The host URL for the XUI API.
        username (str): The username for authentication.
        password (str): The password for authentication.
        client (ClientApi): An instance of the ClientApi class for client interactions.
        inbound (InboundApi): An instance of the InboundApi class for inbound interactions.
        database (DatabaseApi): An instance of the DatabaseApi class for database interactions.
    """

    def __init__(self, host: str, username: str, password: str, skip_login: bool = False):
        """Initialize the Api class with the necessary credentials and login status.

        Args:
            host (str): The host URL for the XUI API.
            username (str): The username for authentication.
            password (str): The password for authentication.
            skip_login (bool, optional): Whether to skip the login process. Defaults to False.
        """
        self.host = host
        self.username = username
        self.password = password
        self.client = ClientApi(host, username, password)
        self.inbound = InboundApi(host, username, password)
        self.database = DatabaseApi(host, username, password)
        if not skip_login:
            self.login()

    @classmethod
    def from_env(cls, skip_login: bool = False) -> Api:
        """Create an instance of the Api class using environment variables for credentials.

        Required environment variables:
            XUI_HOST: The host URL for the XUI API.
            XUI_USERNAME: The username for authentication.
            XUI_PASSWORD: The password for authentication.

        Args:
            skip_login (bool, optional): Whether to skip the login process. Defaults to False.

        Returns:
            Api: An instance of the Api class.

        Examples:
            
            api = Api.from_env()
            
        """
        host = env.xui_host()
        username = env.xui_username()
        password = env.xui_password()
        return cls(host, username, password, skip_login)

    def login(self) -> None:
        """Log in to the XUI API using the provided credentials.

        This method sets the session for the inbound and database APIs to the session of the client API.

        Examples:
            
            api = Api('https://example.com', 'user', 'pass')
            api.login()
            
        """
        self.client.login()
        self.inbound.session = self.client.session
        self.database.session = self.client.session
        logger.info("Logged in successfully.")