from py3xui.client.client import Client
from py3xui.inbound.bases import JsonStringModel


# pylint: disable=too-few-public-methods
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
    """Represents the settings parsed from the XUI API.

    Attributes:
        clients (list[Client]): A list of Client objects.
        decryption (str): A string representing the decryption settings.
        fallbacks (list): A list representing fallbacks.
    """

    clients: list[Client] = []
    decryption: str = ""
    fallbacks: list = []