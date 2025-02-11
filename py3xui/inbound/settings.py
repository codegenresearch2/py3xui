"""
This module provides classes for handling settings retrieved from the XUI API.
"""

from py3xui.client.client import Client
from py3xui.inbound.bases import JsonStringModel


# pylint: disable=too-few-public-methods
class SettingsFields:
    """Stores the fields returned by the XUI API for parsing."""

    CLIENTS = "clients"
    DECRYPTION = "decryption"
    FALLBACKS = "fallbacks"


class Settings(JsonStringModel):
    """Class for storing and parsing settings from the XUI API."""

    clients: list[Client] = []
    """List of Client objects."""

    decryption: str = ""
    """String representing the decryption settings."""

    fallbacks: list = []
    """List of fallbacks."""