"""
This module provides classes for handling settings retrieved from the XUI API.
"""

from typing import List
from py3xui.client.client import Client
from py3xui.inbound.bases import JsonStringModel

# pylint: disable=missing-class-docstring
class SettingsFields:
    """Stores the fields returned by the XUI API for parsing."""

    CLIENTS = "clients"
    DECRYPTION = "decryption"
    FALLBACKS = "fallbacks"


# pylint: disable=missing-docstring, too-few-public-methods
class Settings(JsonStringModel):
    """Class for storing and parsing settings from the XUI API.

    Attributes:
        clients (List[Client]): List of Client objects.
        decryption (str): String representing the decryption settings.
        fallbacks (List): List of fallbacks.
    """

    clients: List[Client] = []
    """List of Client objects."""

    decryption: str = ""
    """String representing the decryption settings."""

    fallbacks: List = []
    """List of fallbacks."""