"""
This module provides a high-level interface to interact with the XUI API.

The `Api` class offers methods to interact with the client, inbound, and database APIs of the XUI system.

Attributes:
    client (ClientApi): An instance of the ClientApi class for client-related operations.
    inbound (InboundApi): An instance of the InboundApi class for inbound-related operations.
    database (DatabaseApi): An instance of the DatabaseApi class for database-related operations.

Examples:
    To create an instance of the Api class using environment variables for credentials:

    
    api = Api.from_env()
    response = api.client.get_client_info()
    print(response)
    

    To manually initialize the Api class with specific credentials:

    
    api = Api('https://xui.example.com', 'user', 'pass')
    api.login()
    print("Logged in successfully.")
    
"""

from __future__ import annotations
from py3xui.api import ClientApi, DatabaseApi, InboundApi
from py3xui.utils import Logger, env

logger = Logger(__name__)


class Api:
    """
    A high-level interface to interact with the XUI API.

    This class provides methods to interact with the client, inbound, and database APIs of the XUI system.

    Attributes:
        client (ClientApi): An instance of the ClientApi class for client-related operations.
        inbound (InboundApi): An instance of the InboundApi class for inbound-related operations.
        database (DatabaseApi): An instance of the DatabaseApi class for database-related operations.
    """

    def __init__(self, host: str, username: str, password: str, skip_login: bool = False):
        """
        Initializes the Api class with the necessary credentials and API instances.

        Args:
            host (str): The XUI host URL for the API.
            username (str): The username for authentication.
            password (str): The password for authentication.
            skip_login (bool, optional): Whether to skip the login process. Defaults to False.

        Attributes:
            client (ClientApi): An instance of the ClientApi class for client-related operations.
            inbound (InboundApi): An instance of the InboundApi class for inbound-related operations.
            database (DatabaseApi): An instance of the DatabaseApi class for database-related operations.
        """
        self.client = ClientApi(host, username, password)
        self.inbound = InboundApi(host, username, password)
        self.database = DatabaseApi(host, username, password)
        if not skip_login:
            self.login()

    @classmethod
    def from_env(cls, skip_login: bool = False) -> Api:
        """
        Creates an instance of the Api class using environment variables for credentials.

        Args:
            skip_login (bool, optional): Whether to skip the login process. Defaults to False.

        Returns:
            Api: An instance of the Api class.

        Notes:
            The following environment variables must be set:
                - XUI_HOST: The XUI host URL for the API.
                - XUI_USERNAME: The username for authentication.
                - XUI_PASSWORD: The password for authentication.
        """
        host = env.xui_host()
        username = env.xui_username()
        password = env.xui_password()
        return cls(host, username, password, skip_login)

    def login(self) -> None:
        """
        Logs into the XUI API using the provided credentials.

        The session is shared across the client, inbound, and database APIs.

        Notes:
            This method logs into the XUI API using the credentials provided during initialization.
            It sets the session for the client, inbound, and database APIs to the session of the client API.
        """
        self.client.login()
        self.inbound.session = self.client.session
        self.database.session = self.client.session
        logger.info("Logged in successfully.")