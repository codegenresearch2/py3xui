from pydantic import ConfigDict, Field\nfrom py3xui.inbound.bases import JsonStringModel\n# pylint: disable=too-few-public-methods\n\nclass StreamSettingsFields:\n    """Stores the fields returned by the XUI API for parsing."""\n    SECURITY = "security"\n    NETWORK = "network"\n    TCP_SETTINGS = "tcpSettings"\n    EXTERNAL_PROXY = "externalProxy"\n    REALITY_SETTINGS = "realitySettings"\n    XTLS_SETTINGS = "xtlsSettings"\n    TLS_SETTINGS = "tlsSettings"\n\nclass StreamSettings(JsonStringModel):\n    """Represents the settings for an inbound connection.\n\n    Attributes:\n        security (str): The security settings for the inbound connection.\n        network (str): The network settings for the inbound connection.\n        tcp_settings (dict): The TCP settings for the inbound connection. Optional.\n        external_proxy (list): The external proxy settings for the inbound connection. Optional.\n        reality_settings (dict): The reality settings for the inbound connection. Optional.\n        xtls_settings (dict): The xtls settings for the inbound connection. Optional.\n        tls_settings (dict): The tls settings for the inbound connection. Optional.\n    """\n\n    security: str\n    network: str\n    tcp_settings: dict = Field(alias=StreamSettingsFields.TCP_SETTINGS)  # type: ignore\n    external_proxy: list = Field(  # type: ignore\n        default=[], alias=StreamSettingsFields.EXTERNAL_PROXY\n    )\n    reality_settings: dict = Field(  # type: ignore\n        default={}, alias=StreamSettingsFields.REALITY_SETTINGS\n    )\n    xtls_settings: dict = Field(  # type: ignore\n        default={}, alias=StreamSettingsFields.XTLS_SETTINGS\n    )\n    tls_settings: dict = Field(default={}, alias=StreamSettingsFields.TLS_SETTINGS)  # type: ignore\n\n    model_config = ConfigDict(\n        populate_by_name=True,\n    )\n