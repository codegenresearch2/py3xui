"""
This module contains the `Inbound` class, which represents the inbound settings for a network service within the XUI API.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from py3xui.client.client import Client
from py3xui.inbound.settings import Settings
from py3xui.inbound.sniffing import Sniffing
from py3xui.inbound.stream_settings import StreamSettings


# Stores the fields returned by the XUI API for parsing.
class InboundFields:
    """Class to store the fields returned by the XUI API for parsing."""
    ENABLE = "enable"
    PORT = "port"
    PROTOCOL = "protocol"
    SETTINGS = "settings"
    STREAM_SETTINGS = "streamSettings"
    SNIFFING = "sniffing"

    ID = "id"
    UP = "up"
    DOWN = "down"
    TOTAL = "total"
    REMARK = "remark"

    EXPIRY_TIME = "expiryTime"
    CLIENT_STATS = "clientStats"
    LISTEN = "listen"

    TAG = "tag"


# pylint: disable=too-few-public-methods
class Inbound(BaseModel):
    """Class representing the inbound settings for a network service within the XUI API.

    Attributes:
        enable (bool): Whether the inbound connection is enabled. (Required)
        port (int): The port number for the inbound connection. (Required)
        protocol (str): The protocol used for the inbound connection. (Required)
        settings (Settings): The settings object for the inbound connection. (Required)
        stream_settings (StreamSettings): The stream settings object for the inbound connection. (Required)
        sniffing (Sniffing): The sniffing object for the inbound connection. (Required)
        listen (str): The listen address for the inbound connection. (Optional)
        remark (str): A remark or description for the inbound connection. (Optional)
        id (int): The ID of the inbound connection. (Optional)
        up (int): The upload speed for the inbound connection. (Optional)
        down (int): The download speed for the inbound connection. (Optional)
        total (int): The total amount of data for the inbound connection. (Optional)
        expiry_time (int): The expiry time for the inbound connection. (Optional)
        client_stats (list[Client]): The list of client statistics for the inbound connection. (Optional)
        tag (str): The tag for the inbound connection. (Optional)
    """

    enable: bool
    port: int
    protocol: str
    settings: Settings
    stream_settings: StreamSettings = Field(alias=InboundFields.STREAM_SETTINGS)  # type: ignore
    sniffing: Sniffing

    listen: str = ""
    remark: str = ""
    id: int = 0

    up: int = 0
    down: int = 0

    total: int = 0

    expiry_time: int = Field(default=0, alias=InboundFields.EXPIRY_TIME)  # type: ignore
    client_stats: list[Client] = Field(default=[], alias=InboundFields.CLIENT_STATS)  # type: ignore

    tag: str = ""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    def to_json(self) -> dict[str, Any]:
        """
        Convert the Inbound object to a JSON dictionary.

        Returns:
            dict: A dictionary representation of the Inbound object.
        """
        include = {
            InboundFields.REMARK,
            InboundFields.ENABLE,
            InboundFields.LISTEN,
            InboundFields.PORT,
            InboundFields.PROTOCOL,
            InboundFields.EXPIRY_TIME,
        }

        result = super().model_dump(by_alias=True)
        result = {k: v for k, v in result.items() if k in include}
        result.update(
            {
                InboundFields.SETTINGS: self.settings.model_dump_json(by_alias=True),
                InboundFields.STREAM_SETTINGS: self.stream_settings.model_dump_json(  # pylint: disable=no-member
                    by_alias=True
                ),
                InboundFields.SNIFFING: self.sniffing.model_dump_json(by_alias=True),
            }
        )

        return result