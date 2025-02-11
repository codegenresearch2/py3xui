"""
This module handles the configuration settings for the inbound connections.
"""

from py3xui.client.client import Client
from py3xui.inbound.bases import JsonStringModel


class SettingsFields:
    """Stores the fields returned by the XUI API for parsing.

    Attributes:
        CLIENTS (str): The field representing clients.
        DECRYPTION (str): The field representing decryption settings.
        FALLBACKS (str): The field representing fallbacks.
    """

    CLIENTS = "clients"
    DECRYPTION = "decryption"
    FALLBACKS = "fallbacks"


class Settings(JsonStringModel):
    """Represents the settings parsed from the XUI API for inbound connections.

    Attributes:
        clients (list[Client], optional): A list of Client objects. Defaults to an empty list.
        decryption (str, optional): A string representing the decryption settings. Defaults to an empty string.
        fallbacks (list, optional): A list representing fallbacks. Defaults to an empty list.
    """

    clients: list[Client] = []
    decryption: str = ""
    fallbacks: list = []