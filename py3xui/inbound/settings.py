"""
This module provides classes for parsing settings from the XUI API.
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
    """
    Class representing the settings for an inbound connection.

    Attributes:
        clients (List[Client]): List of Client objects.
        decryption (str): String representing the decryption settings.
        fallbacks (list): List of fallbacks.
    """

    clients: List[Client] = []
    """List of Client objects."""

    decryption: str = ""
    """String representing the decryption settings."""

    fallbacks: list = []
    """List of fallbacks."""