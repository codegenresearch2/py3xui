'''This module contains the Sniffing class, which represents sniffing settings in the XUI API.'''nfrom pydantic import Fieldnfrom py3xui.inbound.bases import JsonStringModeln# pylint: disable=too-few-public-methodsnclass SniffingFields:n    '''Stores the fields returned by the XUI API for parsing.'''n    ENABLED = 'enabled'n    DEST_OVERRIDE = 'destOverride'n    METADATA_ONLY = 'metadataOnly'n    ROUTE_ONLY = 'routeOnly'nclass Sniffing(JsonStringModel):n    '''Represents sniffing settings for the XUI API.n    Attributes:n        enabled (bool): Whether sniffing is enabled. Required.n        dest_override (list[str]): List of destination overrides. Optional.n        metadata_only (bool): Whether to only sniff metadata. Optional.n        route_only (bool): Whether to only route the traffic. Optional.n    '''n    enabled: booln    dest_override: list[str] = Field(default=[], alias=SniffingFields.DEST_OVERRIDE)  # type: ignoren    metadata_only: bool = Field(default=False, alias=SniffingFields.METADATA_ONLY)  # type: ignoren    route_only: bool = Field(default=False, alias=SniffingFields.ROUTE_ONLY)  # type: ignore