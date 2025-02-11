"""
This module provides a high-level interface to interact with the XUI API.

The module includes classes for managing client, inbound, and database interactions through the XUI API.

Public Classes:
    Api: A class to interact with the XUI API.

Private Classes:
    ClientApi: A class to interact with the client API.
    InboundApi: A class to interact with the inbound API.
    DatabaseApi: A class to interact with the database API.

Public Methods:
    login: Logs into the XUI API.
    from_env: Creates an instance of the API from environment variables.

Attributes:
    client (ClientApi): The client API.
    inbound (InboundApi): The inbound API.
    database (DatabaseApi): The database API.
"""

from __future__ import annotations

from py3xui.api import ClientApi, DatabaseApi, InboundApi
from py3xui.utils import Logger, env

logger = Logger(__name__)


class Api:
    """This class provides a high-level interface to interact with the XUI API.

    Access to the client, inbound, and database APIs is provided through this class.

    Args:
        host (str): The XUI host URL.
        username (str): The XUI username.
        password (str): The XUI password.
        skip_login (bool): Skip the login process. Default is False.

    Attributes:
        client (ClientApi): The client API.
        inbound (InboundApi): The inbound API.
        database (DatabaseApi): The database API.
    """

    def __init__(self, host: str, username: str, password: str, skip_login: bool = False):
        """Initializes the Api instance.

        Args:
            host (str): The XUI host URL.
            username (str): The XUI username.
            password (str): The XUI password.
            skip_login (bool): Skip the login process. Default is False.
        """
        self.client = ClientApi(host, username, password)
        self.inbound = InboundApi(host, username, password)
        self.database = DatabaseApi(host, username, password)
        if not skip_login:
            self.login()

    @classmethod
    def from_env(cls, skip_login: bool = False) -> Api:
        """Creates an instance of the API from environment variables.

        Following environment variables should be set:
        - XUI_HOST: The XUI host URL.
        - XUI_USERNAME: The XUI username.
        - XUI_PASSWORD: The XUI password.

        Args:
            skip_login (bool): Skip the login process. Default is False.

        Returns:
            Api: The API instance.
        """
        host = env.xui_host()
        username = env.xui_username()
        password = env.xui_password()
        return cls(host, username, password, skip_login)

    def login(self) -> None:
        """Logs into the XUI API and sets the session cookie for the client, inbound, and database APIs.

        Raises:
            ValueError: If the login is unsuccessful.
        """
        self.client.login()
        self.inbound.session = self.client.session
        self.database.session = self.client.session
        logger.info("Logged in successfully.")