from pydantic import Field


# pylint: disable=too-few-public-methods
class SniffingFields:
    """Stores the fields returned by the XUI API for parsing."""

    ENABLED = "enabled"

    DEST_OVERRIDE = "destOverride"

    METADATA_ONLY = "metadataOnly"
    ROUTE_ONLY = "routeOnly"


class Sniffing:
    """Represents sniffing settings for inbound connections in the XUI API.

    Attributes:
        enabled (bool): Whether sniffing is enabled. Required.
        dest_override (list[str]): List of destination overrides for sniffing. Optional.
        metadata_only (bool): Whether to only sniff metadata. Optional.
        route_only (bool): Whether to only route the sniffed traffic. Optional.
    """

    def __init__(self, enabled: bool, dest_override: list[str] = [], metadata_only: bool = False, route_only: bool = False):
        """Initializes the Sniffing class.

        Args:
            enabled (bool): Whether sniffing is enabled.
            dest_override (list[str], optional): List of destination overrides for sniffing. Defaults to an empty list.
            metadata_only (bool, optional): Whether to only sniff metadata. Defaults to False.
            route_only (bool, optional): Whether to only route the sniffed traffic. Defaults to False.
        """
        self.enabled = enabled
        self.dest_override = dest_override
        self.metadata_only = metadata_only
        self.route_only = route_only

    def to_json(self) -> dict:
        """Converts the Sniffing instance to a JSON-compatible dictionary for the XUI API.

        Returns:
            dict: The JSON-compatible dictionary.
        """
        return {
            SniffingFields.ENABLED: self.enabled,
            SniffingFields.DEST_OVERRIDE: self.dest_override,
            SniffingFields.METADATA_ONLY: self.metadata_only,
            SniffingFields.ROUTE_ONLY: self.route_only,
        }