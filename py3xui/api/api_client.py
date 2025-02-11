import json
from typing import List, Optional
from py3xui.api.api_base import ApiFields, BaseApi
from py3xui.client.client import Client
from py3xui.utils import Logger

logger = Logger(__name__)


class ClientApi(BaseApi):
    def get_by_email(self, email: str) -> Optional[Client]:
        """Retrieves information about a specific client based on their email.

        This endpoint provides details such as traffic statistics and other relevant information
        related to the client.

        Args:
            email (str): The email of the client to retrieve.

        Returns:
            Optional[Client]: The client object if found, otherwise None.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            client: py3xui.Client = api.get_by_email("email")
            
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

    def get_ips(self, email: str) -> Optional[str]:
        """Retrieves the IP records associated with a specific client identified by their email.

        Args:
            email (str): The email of the client to retrieve.

        Returns:
            Optional[str]: The client IPs if found, otherwise None.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            ips = api.get_ips("email")
            
        """
        endpoint = f"panel/api/inbounds/clientIps/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        logger.info("Getting client IPs for email: %s", email)

        response = self._post(url, headers, {})

        ips_json = response.json().get(ApiFields.OBJ)
        return ips_json if ips_json != ApiFields.NO_IP_RECORD else None

    def add(self, inbound_id: int, clients: List[Client]):
        """Adds a list of clients to a specific inbound.

        Args:
            inbound_id (int): The ID of the inbound to which clients will be added.
            clients (List[Client]): The list of clients to be added.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            clients = [...]  # List of Client objects
            api.add(inbound_id, clients)
            
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
        """Updates a client's information.

        Args:
            client_uuid (str): The UUID of the client to update.
            client (Client): The updated client object.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            updated_client = py3xui.Client(...)  # Updated client object
            api.update(client_uuid, updated_client)
            
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
        """Resets the IP records associated with a specific client identified by their email.

        Args:
            email (str): The email of the client whose IPs will be reset.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            api.reset_ips("email")
            
        """
        endpoint = f"panel/api/inbounds/clearClientIps/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Resetting client IPs for email: %s", email)

        self._post(url, headers, data)
        logger.info("Client IPs reset successfully.")

    def reset_stats(self, inbound_id: int, email: str) -> None:
        """Resets the traffic statistics for a specific client identified by their email.

        Args:
            inbound_id (int): The ID of the inbound to which the client belongs.
            email (str): The email of the client whose stats will be reset.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            api.reset_stats(inbound_id, "email")
            
        """
        endpoint = f"panel/api/inbounds/{inbound_id}/resetClientTraffic/{email}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Resetting client stats for inbound ID: %s, email: %s", inbound_id, email)

        self._post(url, headers, data)
        logger.info("Client stats reset successfully.")

    def delete(self, inbound_id: int, client_uuid: str) -> None:
        """Deletes a specific client from an inbound.

        Args:
            inbound_id (int): The ID of the inbound from which the client will be deleted.
            client_uuid (str): The UUID of the client to be deleted.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            api.delete(inbound_id, client_uuid)
            
        """
        endpoint = f"panel/api/inbounds/{inbound_id}/delClient/{client_uuid}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Deleting client with ID: %s", client_uuid)

        self._post(url, headers, data)
        logger.info("Client deleted successfully.")

    def delete_depleted(self, inbound_id: int) -> None:
        """Deletes all depleted clients from a specific inbound.

        Args:
            inbound_id (int): The ID of the inbound from which depleted clients will be deleted.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            api.delete_depleted(inbound_id)
            
        """
        endpoint = f"panel/api/inbounds/delDepletedClients/{inbound_id}"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Deleting depleted clients for inbound ID: %s", inbound_id)

        self._post(url, headers, data)
        logger.info("Depleted clients deleted successfully.")

    def online(self) -> List[str]:
        """Retrieves a list of online clients.

        Returns:
            List[str]: A list of emails of online clients.

        Examples:
            
            import py3xui

            api = py3xui.Api.from_env()
            online_clients = api.online()
            
        """
        endpoint = "panel/api/inbounds/onlines"
        headers = {"Accept": "application/json"}

        url = self._url(endpoint)
        data: dict[str, Any] = {}
        logger.info("Getting online clients")

        response = self._post(url, headers, data)
        online = response.json().get(ApiFields.OBJ)
        return online or []


This revised code snippet addresses the feedback provided by the oracle. It includes the necessary changes to return type annotations, improve docstring formatting, and ensure consistent logging messages. The examples are also formatted using triple backticks for better readability.