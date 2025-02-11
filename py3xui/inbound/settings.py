"""
This module contains the `Settings` class for parsing JSON responses from the XUI API.
"""

from typing import List
from py3xui.client.client import Client
from py3xui.inbound.bases import JsonStringModel

# pylint: disable=too-few-public-methods
class SettingsFields:
    """Stores the fields returned by the XUI API for parsing."""

    CLIENTS = "clients"
    DECRYPTION = "decryption"
    FALLBACKS = "fallbacks"


class Settings(JsonStringModel):
    """Class representing settings for an inbound connection.

    Attributes:
        clients (List[Client]): List of Client objects related to inbound connections.
        decryption (str): String representing the decryption settings for inbound connections.
        fallbacks (List): List of fallbacks related to inbound connections.
    """

    clients: List[Client] = []
    """List of Client objects related to inbound connections."""

    decryption: str = ""
    """String representing the decryption settings for inbound connections."""

    fallbacks: List = []
    """List of fallbacks related to inbound connections."""