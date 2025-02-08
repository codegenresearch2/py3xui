from pydantic import Field\\n\\n# pylint: disable=too-few-public-methods\\nclass SniffingFields:\\n    """Stores the fields returned by the XUI API for parsing."""\\n    ENABLED = "enabled"\\n    DEST_OVERRIDE = "destOverride"\\n    METADATA_ONLY = "metadataOnly"\\n    ROUTE_ONLY = "routeOnly"\\n\\nclass Sniffing(JsonStringModel):\\n    """Represents sniffing settings in the XUI API.\\n\\n    Attributes:\\n        enabled (bool): Whether sniffing is enabled. Required.\\n        dest_override (list[str]): The destination overrides for sniffing. Optional.\\n        metadata_only (bool): Whether to only sniff metadata. Optional. Default is False.\\n        route_only (bool): Whether to only route the sniffed traffic. Optional. Default is False.\"""\\n        enabled: bool\\n        dest_override: list[str] = Field(default=[], alias=SniffingFields.DEST_OVERRIDE)  # type: ignore\\n        metadata_only: bool = Field(default=False, alias=SniffingFields.METADATA_ONLY)  # type: ignore\\n        route_only: bool = Field(default=False, alias=SniffingFields.ROUTE_ONLY)  # type: ignore\\n