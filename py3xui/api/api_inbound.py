import logging
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Inbound:
    '''
    A class representing an inbound object.
    '''
    def __init__(self, id: int, enable: bool, port: int, protocol: str, settings: dict, stream_settings: dict, sniffing: dict, remark: Optional[str] = None):
        '''
        Initializes an Inbound object.

        Args:
            id (int): The ID of the inbound.
            enable (bool): Whether the inbound is enabled.
            port (int): The port number.
            protocol (str): The protocol used.
            settings (dict): The settings for the inbound.
            stream_settings (dict): The stream settings for the inbound.
            sniffing (dict): The sniffing settings for the inbound.
            remark (Optional[str]): An optional remark for the inbound.
        '''
        self.id = id
        self.enable = enable
        self.port = port
        self.protocol = protocol
        self.settings = settings
        self.stream_settings = stream_settings
        self.sniffing = sniffing
        self.remark = remark

class InboundApi:
    '''
    A class to interact with the Inbound API.
    '''
    def __init__(self, host: str, username: str, password: str):
        '''
        Initializes the InboundApi class with the necessary credentials and host.

        Args:
            host (str): The API host URL.
            username (str): The API username.
            password (str): The API password.
        '''
        self.host = host
        self.username = username
        self.password = password
        self.session = self._create_session()

    def _create_session(self):
        '''
        Creates a session object for making API requests.

        Returns:
            requests.Session: A session object.
        '''
        import requests
        session = requests.Session()
        session.auth = (self.username, self.password)
        return session

    def get_list(self) -> List[Inbound]:
        '''
        Retrieves a list of inbounds from the API.

        Returns:
            List[Inbound]: A list of Inbound objects.
        '''
        endpoint = f'{self.host}/panel/api/inbounds/list'
        logger.info('Retrieving inbounds from %s',
                    endpoint)
        response = self.session.get(endpoint)
        response.raise_for_status()
        inbounds_json = response.json().get('obj', [])
        inbounds = [Inbound(**data) for data in inbounds_json]
        return inbounds

    def add(self, inbound: Inbound) -> None:
        '''
        Adds a new inbound to the API.

        Args:
            inbound (Inbound): The Inbound object to add.
        '''
        endpoint = f'{self.host}/panel/api/inbounds/add'
        logger.info('Adding inbound to %s',
                    endpoint)
        data = inbound.__dict__
        response = self.session.post(endpoint, json=data)
        response.raise_for_status()
        logger.info('Inbound added successfully')

    def delete(self, inbound_id: int) -> None:
        '''
        Deletes an inbound from the API by its ID.

        Args:
            inbound_id (int): The ID of the inbound to delete.
        '''
        endpoint = f'{self.host}/panel/api/inbounds/del/{inbound_id}',
        logger.info('Deleting inbound with ID %s from %s',
                    inbound_id, endpoint)
        response = self.session.post(endpoint)
        response.raise_for_status()
        logger.info('Inbound deleted successfully')

    def update(self, inbound_id: int, inbound: Inbound) -> None:
        '''
        Updates an existing inbound in the API.

        Args:
            inbound_id (int): The ID of the inbound to update.
            inbound (Inbound): The updated Inbound object.
        '''
        endpoint = f'{self.host}/panel/api/inbounds/update/{inbound_id}',
        logger.info('Updating inbound with ID %s at %s',
                    inbound_id, endpoint)
        data = inbound.__dict__
        response = self.session.post(endpoint, json=data)
        response.raise_for_status()
        logger.info('Inbound updated successfully')