"""
This module provides classes for parsing JSON responses from the XUI API.
"""

from typing import List
from py3xui.client.client import Client
from py3xui.inbound.bases import JsonStringModel


class SettingsFields:
    """Stores the fields returned by the XUI API for parsing."""

    CLIENTS = "clients"
    DECRYPTION = "decryption"
    FALLBACKS = "fallbacks"


class Settings(JsonStringModel):
    """Class for storing and parsing settings from the XUI API.

    Attributes:
        clients (List[Client]): List of Client objects related to inbound connections.
        decryption (str): String representing the decryption settings for inbound connections.
        fallbacks (List): List of fallbacks related to inbound connections.
    """

    clients: List[Client] = []
    decryption: str = ""
    fallbacks: List = []