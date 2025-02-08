import json
from typing import Any

from py3xui.api.api_base import ApiFields, BaseApi
from py3xui.client.client import Client
from py3xui.utils import Logger

logger = Logger(__name__)


class ClientApi(BaseApi):
    def get_by_email(self, email: str) -> Client | None:
        '''This route is used to retrieve information about a specific client based on their email.
        This endpoint provides details such as traffic statistics and other relevant information
        related to the client.

        `Source documentation <https://documenter.getpostman.com/view/16802678/2s9YkgD5jm#9d0e5cd5-e6ac-4d72-abca-76cf75af5f00>`_

        Args:
            email (str): The email of the client to retrieve.

        Returns:
            Client | None: The client object if found, otherwise None.

        Examples::
            import py3xui

            api = py3xui.Api.from_env()
            client = api.client.get_by_email("email")
        '''
        endpoint = f"panel/api/inbounds/getClientTraffics/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        logger.info("Getting client stats for email: %s", email)

        response = self._get(url, headers)

        client_json = response.json().get(ApiFields.OBJ)
        if not client_json:
            logger.warning("No client found for email: %s", email)
            return None
        return Client.model_validate(client_json)

    def get_ips(self, email: str) -> str | None:
        '''This route is used to retrieve the IP records associated with a specific client
        identified by their email.

        `Source documentation <https://documenter.getpostman.com/view/16802678/2s9YkgD5jm#06f1214c-dbb0-49f2-81b5-8e924abd19a9>`_

        Args:
            email (str): The email of the client to retrieve.

        Returns:
            str | None: The client IPs if found, otherwise None.

        Examples::
            import py3xui

            api = py3xui.Api.from_env()
            ips = api.client.get_ips("email")
        '''
        endpoint = f"panel/api/inbounds/clientIps/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        logger.info("Getting client IPs for email: %s", email)

        response = self._post(url, headers, {})

        ips_json = response.json().get(ApiFields.OBJ)
        return ips_json if ips_json != ApiFields.NO_IP_RECORD else None

    def add(self, inbound_id: int, clients: list[Client]):
        '''Add clients to an inbound.

        Args:
            inbound_id (int): The ID of the inbound to which clients will be added.
            clients (list[Client]): A list of Client objects to be added.

        Examples::
            import py3xui

            api = py3xui.Api.from_env()
            clients = [...]  # List of Client objects
            api.client.add(inbound_id, clients)
        '''
        endpoint = "panel/api/inbounds/addClient"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        settings = [client.model_dump(by_alias=True, exclude_defaults=True) for client in clients]
        data = {"id": inbound_id, "settings": json.dumps({"clients": settings})}
        logger.info("Adding %s clients to inbound with ID: %s", len(clients), inbound_id)

        self._post(url, headers, data)
        logger.info("Client added successfully.")

    # Additional methods omitted for brevity
