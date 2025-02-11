"""This module contains the Sniffing class, which represents sniffing settings in the XUI API."""

from pydantic import Field

from py3xui.inbound.bases import JsonStringModel


# pylint: disable=too-few-public-methods
class SniffingFields:
    """Stores the fields returned by the XUI API for parsing."""

    ENABLED = "enabled"

    DEST_OVERRIDE = "destOverride"

    METADATA_ONLY = "metadataOnly"
    ROUTE_ONLY = "routeOnly"


class Sniffing(JsonStringModel):
    """Represents sniffing settings in the XUI API.

    Attributes:
        enabled (bool): Whether sniffing is enabled. Required.
        dest_override (list[str]): The destination overrides for sniffing. Optional.
        metadata_only (bool): Whether to only sniff metadata. Optional.
        route_only (bool): Whether to only route the sniffed traffic. Optional.
    """

    enabled: bool

    dest_override: list[str] = Field(default=[], alias=SniffingFields.DEST_OVERRIDE)  # type: ignore

    metadata_only: bool = Field(default=False, alias=SniffingFields.METADATA_ONLY)  # type: ignore
    route_only: bool = Field(default=False, alias=SniffingFields.ROUTE_ONLY)  # type: ignore