from pydantic import BaseModel, Field, ConfigDict\nfrom typing import Any, Optional\nfrom py3xui.client.client import Client\nfrom py3xui.inbound.settings import Settings\nfrom py3xui.inbound.sniffing import Sniffing\nfrom py3xui.inbound.stream_settings import StreamSettings\n\n# pylint: disable=too-few-public-methods\nclass InboundFields:\n    '''Class to define constants for inbound fields.''' \n    ENABLE = 'enable'\n    PORT = 'port'\n    PROTOCOL = 'protocol'\n    SETTINGS = 'settings'\n    STREAM_SETTINGS = 'streamSettings'\n    SNIFFING = 'sniffing'\n    LISTEN = 'listen'\n    REMARK = 'remark'\n    ID = 'id'\n    UP = 'up'\n    DOWN = 'down'\n    TOTAL = 'total'\n    EXPIRY_TIME = 'expiryTime'\n    CLIENT_STATS = 'clientStats'\n    TAG = 'tag'\n\nclass Inbound(BaseModel):\n    '''Represents an inbound connection in the XUI API.''' \n    enable: bool\n    port: int\n    protocol: str\n    settings: Settings\n    stream_settings: StreamSettings = Field(alias=InboundFields.STREAM_SETTINGS)  # type: ignore\n    sniffing: Sniffing\n    listen: str = ''\n    remark: str = ''\n    id: int = 0\n    up: int = 0\n    down: int = 0\n    total: int = 0\n    expiry_time: int = Field(default=0, alias=InboundFields.EXPIRY_TIME)  # type: ignore\n    client_stats: list[Client] | None = Field(default=[], alias=InboundFields.CLIENT_STATS)  # type: ignore\n    tag: str = ''\n    model_config = ConfigDict(populate_by_name=True)\n\n    def to_json(self) -> dict[str, Any]:\n        '''\n        Converts the Inbound instance to a JSON-compatible dictionary for the XUI API.\n        \n        Returns:\n            dict[str, Any]: The JSON-compatible dictionary.\n        '''\n        include = {\n            InboundFields.REMARK,\n            InboundFields.ENABLE,\n            InboundFields.LISTEN,\n            InboundFields.PORT,\n            InboundFields.PROTOCOL,\n            InboundFields.EXPIRY_TIME,\n        }\n        result = super().model_dump(by_alias=True)\n        result = {k: v for k, v in result.items() if k in include}\n        result.update(\n            {\n                InboundFields.SETTINGS: self.settings.model_dump_json(by_alias=True),\n                InboundFields.STREAM_SETTINGS: self.stream_settings.model_dump_json(  # pylint: disable=no-member\n                    by_alias=True\n                ),\n                InboundFields.SNIFFING: self.sniffing.model_dump_json(by_alias=True),\n            }\n        )\n        return result\n    }