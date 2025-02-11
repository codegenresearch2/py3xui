import json
from typing import Any

from py3xui.api.api_base import ApiFields, BaseApi
from py3xui.client.client import Client
from py3xui.utils import Logger

logger = Logger(__name__)


class ClientApi(BaseApi):
    def get_by_email(self, email: str) -> Client | None:
        """Retrieve information about a specific client based on their email.

        This endpoint provides details such as traffic statistics and other relevant information
        related to the client.

        Args:
            email (str): The email of the client to retrieve.

        Returns:
            Client | None: The client object if found, otherwise None.
        """
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
        """Retrieve the IP records associated with a specific client identified by their email.

        Args:
            email (str): The email of the client to retrieve.

        Returns:
            str | None: The client IPs if found, otherwise None.
        """
        endpoint = f"panel/api/inbounds/clientIps/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        logger.info("Getting client IPs for email: %s", email)

        response = self._post(url, headers, {})

        ips_json = response.json().get(ApiFields.OBJ)
        return ips_json if ips_json != ApiFields.NO_IP_RECORD else None

    def add(self, inbound_id: int, clients: list[Client]):
        """Add clients to a specific inbound.

        Args:
            inbound_id (int): The ID of the inbound to which clients will be added.
            clients (list[Client]): List of Client objects to be added.
        """
        endpoint = "panel/api/inbounds/addClient"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        settings = {
            "clients": [
                client.model_dump(by_alias=True, exclude_defaults=True) for client in clients
            ]
        }
        data = {"id": inbound_id, "settings": json.dumps(settings)}
        logger.info("Adding %s clients to inbound with ID: %s", len(clients), inbound_id)

        self._post(url, headers, data)
        logger.info("Client added successfully.")

    def update(self, client_uuid: str, client: Client) -> None:
        """Update a specific client.

        Args:
            client_uuid (str): The UUID of the client to update.
            client (Client): The updated Client object.
        """
        endpoint = f"panel/api/inbounds/updateClient/{client_uuid}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        settings = {"clients": [client.model_dump(by_alias=True, exclude_defaults=True)]}
        data = {"id": client.inbound_id, "settings": json.dumps(settings)}

        logger.info("Updating client: %s", client)
        self._post(url, headers, data)
        logger.info("Client updated successfully.")

    def reset_ips(self, email: str) -> None:
        """Reset the IP records associated with a specific client identified by their email.

        Args:
            email (str): The email of the client whose IPs will be reset.
        """
        endpoint = f"panel/api/inbounds/clearClientIps/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Resetting client IPs for email: %s", email)

        self._post(url, headers, data)
        logger.info("Client IPs reset successfully.")

    def reset_stats(self, inbound_id: int, email: str) -> None:
        """Reset the traffic statistics for a specific client.

        Args:
            inbound_id (int): The ID of the inbound to which the client belongs.
            email (str): The email of the client whose stats will be reset.
        """
        endpoint = f"panel/api/inbounds/{inbound_id}/resetClientTraffic/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Resetting client stats for inbound ID: %s, email: %s", inbound_id, email)

        self._post(url, headers, data)
        logger.info("Client stats reset successfully.")

    def delete(self, inbound_id: int, client_uuid: str) -> None:
        """Delete a specific client.

        Args:
            inbound_id (int): The ID of the inbound to which the client belongs.
            client_uuid (str): The UUID of the client to delete.
        """
        endpoint = f"panel/api/inbounds/{inbound_id}/delClient/{client_uuid}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Deleting client with ID: %s", client_uuid)

        self._post(url, headers, data)
        logger.info("Client deleted successfully.")

    def delete_depleted(self, inbound_id: int) -> None:
        """Delete depleted clients from a specific inbound.

        Args:
            inbound_id (int): The ID of the inbound from which depleted clients will be deleted.
        """
        endpoint = f"panel/api/inbounds/delDepletedClients/{inbound_id}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Deleting depleted clients for inbound ID: %s", inbound_id)

        self._post(url, headers, data)
        logger.info("Depleted clients deleted successfully.")

    def online(self) -> list[str]:
        """Get the list of online clients.

        Returns:
            list[str]: List of online clients' emails.
        """
        endpoint = "panel/api/inbounds/onlines"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Getting online clients")

        response = self._post(url, headers, data)
        online = response.json().get(ApiFields.OBJ)
        return online or []