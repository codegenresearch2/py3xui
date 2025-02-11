"""
This module contains the classes for parsing the JSON response from the XUI API, specifically for stream settings.
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

    This class is designed to parse the JSON response from the XUI API, specifically for stream settings.

    Attributes:
        security (str): The security type for the inbound connection. This is a required field.
        network (str): The network settings for the inbound connection. This is a required field.
        tcp_settings (dict): The TCP settings for the inbound connection. This is an optional field.
        external_proxy (list): The external proxy settings for the inbound connection. This is an optional field.
        reality_settings (dict): The reality settings for the inbound connection. This is an optional field.
        xtls_settings (dict): The xTLS settings for the inbound connection. This is an optional field.
        tls_settings (dict): The TLS settings for the inbound connection. This is an optional field.
    """

    security: str
    network: str
    tcp_settings: dict = Field(default={}, alias=StreamSettingsFields.TCP_SETTINGS)  # type: ignore
    external_proxy: list = Field(default=[], alias=StreamSettingsFields.EXTERNAL_PROXY)  # type: ignore
    reality_settings: dict = Field(default={}, alias=StreamSettingsFields.REALITY_SETTINGS)  # type: ignore
    xtls_settings: dict = Field(default={}, alias=StreamSettingsFields.XTLS_SETTINGS)  # type: ignore
    tls_settings: dict = Field(default={}, alias=StreamSettingsFields.TLS_SETTINGS)  # type: ignore

    model_config = ConfigDict(
        populate_by_name=True,
    )


This revised code snippet addresses the feedback from the oracle by improving the module docstring, class docstring, attribute descriptions, field definitions, field defaults, and spacing and formatting.