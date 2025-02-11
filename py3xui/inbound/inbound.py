from typing import Any
from pydantic import BaseModel, ConfigDict, Field

# Stores the fields returned by the XUI API for parsing.
class InboundFields:
    """Stores the fields returned by the XUI API for parsing.
    
    Attributes:
        ENABLE (str): Indicates whether the inbound is enabled.
        PORT (str): The port number for the inbound connection.
        PROTOCOL (str): The protocol used for the inbound connection.
        SETTINGS (str): The settings for the inbound connection.
        STREAM_SETTINGS (str): The stream settings for the inbound connection.
        SNIFFING (str): The sniffing settings for the inbound connection.
        ID (str): The ID of the inbound connection.
        UP (str): The upload limit for the inbound connection.
        DOWN (str): The download limit for the inbound connection.
        TOTAL (str): The total limit for the inbound connection.
        REMARK (str): A remark or description for the inbound connection.
        EXPIRY_TIME (str): The expiry time for the inbound connection.
        CLIENT_STATS (str): The client statistics for the inbound connection.
        LISTEN (str): The listen address for the inbound connection.
        TAG (str): The tag for the inbound connection.
    """
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


class Inbound(BaseModel):
    """Inbound class representing the inbound settings.

    Attributes:
        enable (bool): Indicates whether the inbound is enabled.
        port (int): The port number for the inbound connection.
        protocol (str): The protocol used for the inbound connection.
        settings (Settings): The settings for the inbound connection.
        stream_settings (StreamSettings): The stream settings for the inbound connection.
        sniffing (Sniffing): The sniffing settings for the inbound connection.
        listen (str, optional): The listen address for the inbound connection. Defaults to "".
        remark (str, optional): A remark or description for the inbound connection. Defaults to "".
        id (int, optional): The ID of the inbound connection. Defaults to 0.
        up (int, optional): The upload limit for the inbound connection. Defaults to 0.
        down (int, optional): The download limit for the inbound connection. Defaults to 0.
        total (int, optional): The total limit for the inbound connection. Defaults to 0.
        expiry_time (int, optional): The expiry time for the inbound connection. Defaults to 0.
        client_stats (list[Client], optional): The client statistics for the inbound connection. Defaults to [].
        tag (str, optional): The tag for the inbound connection. Defaults to "".
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
        """Convert the Inbound object to a JSON-compatible dictionary for the XUI API.

        Returns:
            dict: A JSON-compatible dictionary representation of the Inbound object.
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