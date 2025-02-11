"""
This module provides classes for parsing settings from the XUI API.
"""
from typing import List, Optional
from py3xui.client.client import Client
from py3xui.inbound.bases import JsonStringModel


# pylint: disable=too-few-public-methods
class SettingsFields:
    """Stores the fields returned by the XUI API for parsing."""

    CLIENTS = "clients"
    DECRYPTION = "decryption"
    FALLBACKS = "fallbacks"


class Settings(JsonStringModel):
    """
    Class representing the settings for an inbound connection.

    Attributes:
        clients (Optional[List[Client]]): List of Client objects.
        decryption (Optional[str]): String representing the decryption settings.
        fallbacks (Optional[list]): List of fallbacks.
    """

    clients: Optional[List[Client]] = []
    """List of Client objects."""

    decryption: Optional[str] = ""
    """String representing the decryption settings."""

    fallbacks: Optional[list] = []
    """List of fallbacks."""