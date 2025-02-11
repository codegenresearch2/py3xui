"""
This module contains the StreamSettings class, which is used to parse the JSON response
from the XUI API for stream settings.
"""

from pydantic import ConfigDict, Field

from py3xui.inbound.bases import JsonStringModel


# pylint: disable=too-few-public-methods
class StreamSettingsFields:
    """Stores the fields returned by the XUI API for parsing."""

    SECURITY = "security"
    NETWORK = "network"
    TCP_SETTINGS = "tcpSettings"

    EXTERNAL_PROXY = "externalProxy"

    REALITY_SETTINGS = "realitySettings"
    XTLS_SETTINGS = "xtlsSettings"
    TLS_SETTINGS = "tlsSettings"


class StreamSettings(JsonStringModel):
    """Represents the stream settings for an inbound connection.

    Attributes:
        security (str): The security settings for the inbound connection. Required.
        network (str): The network settings for the inbound connection. Required.
        tcp_settings (dict): The TCP settings for the inbound connection. Optional.
        external_proxy (list): The external proxy settings for the inbound connection. Optional.
        reality_settings (dict): The reality settings for the inbound connection. Optional.
        xtls_settings (dict): The xtls settings for the inbound connection. Optional.
        tls_settings (dict): The TLS settings for the inbound connection. Optional.
    """

    security: str
    network: str
    tcp_settings: dict = Field(default_factory=dict)  # type: ignore

    external_proxy: list = Field(default_factory=list)  # type: ignore

    reality_settings: dict = Field(default_factory=dict)  # type: ignore
    xtls_settings: dict = Field(default_factory=dict)  # type: ignore
    tls_settings: dict = Field(default_factory=dict)  # type: ignore

    model_config = ConfigDict(
        populate_by_name=True,
    )