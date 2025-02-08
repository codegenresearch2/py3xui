from typing import List, Optional

from py3xui.api.api_base import ApiFields, BaseApi
from py3xui.inbound import Inbound


class InboundApi(BaseApi):
    """This class provides methods to interact with the inbounds in the XUI API."

    Attributes and Properties:
        host (str): The XUI host URL.
        username (str): The XUI username.
        password (str): The XUI password.
        token (str | None): The XUI secret token.
        use_tls_verify (bool): Whether to verify the server TLS certificate.
        custom_certificate_path (str | None): Path to a custom certificate file.
        session (requests.Session): The session object for the API.
        max_retries (int): The maximum number of retries for the API requests.

    Public Methods:
        get_list: Retrieves a list of inbounds.
        add: Adds a new inbound.
        delete: Deletes an inbound.
        update: Updates an inbound.
        reset_stats: Resets the statistics of all inbounds.
        reset_client_stats: Resets the statistics of a specific inbound.
        get_by_id: Retrieves a specific inbound by its ID.

    Examples:
        \"\"\"python
        import py3xui

        api = py3xui.Api.from_env()
        api.login()

        inbounds: list[py3xui.Inbound] = api.inbound.get_list()
        \"\"\"
    """

    def get_list(self) -> list[Inbound]:
        """This route is used to retrieve a comprehensive list of all inbounds along with
        their associated client options and statistics."

        [Source documentation](https://documenter.getpostman.com/view/16802678/2s9YkgD5jm#b7c42b67-4362-44d3-bd61-ba7df0721802)

        Returns:
            list[Inbound]: A list of inbounds.

        Examples:
            \"\"\"python
            import py3xui

            api = py3xui.Api.from_env()
            api.login()

            inbounds: list[py3xui.Inbound] = api.inbound.get_list()
            \"\"\"
        """
        endpoint = "panel/api/inbounds/list"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        self.logger.info("Getting inbounds...")        

        response = self._get(url, headers)

        inbounds_json = response.json().get(ApiFields.OBJ)
        inbounds = [Inbound.model_validate(data) for data in inbounds_json]
        return inbounds

    # Add other methods similarly updated...
