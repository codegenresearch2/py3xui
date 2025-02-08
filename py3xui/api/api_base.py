from __future__ import annotations

from typing import Any, Callable
import requests
from time import sleep

from py3xui.utils import Logger

logger = Logger(__name__)


class ApiFields:
    '''Stores the fields returned by the XUI API for parsing."
    SUCCESS = "success"
    MSG = "msg"
    OBJ = "obj"
    CLIENT_STATS = "clientStats"
    NO_IP_RECORD = "No IP Record"


class BaseApi:
    '''This class provides a base API for interacting with the XUI API."

    # pylint: disable=too-few-public-methods

    def __init__(self, host: str, username: str, password: str):
        '''Initializes the BaseApi instance.

        Args:
            host (str): The XUI host URL.
            username (str): The XUI username.
            password (str): The XUI password.
        '''
        self._host = host.rstrip("/")
        self._username = username
        self._password = password
        self._max_retries: int = 3
        self._session: str | None = None

    @property
    def host(self) -> str:
        '''The XUI host URL.'''   
        return self._host

    @property
    def username(self) -> str:
        '''The XUI username.'''   
        return self._username

    @property
    def password(self) -> str:
        '''The XUI password.'''   
        return self._password

    @property
    def max_retries(self) -> int:
        '''The maximum number of retries for API requests.'''   
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        '''Sets the maximum number of retries for API requests.

        Args:
            value (int): The new maximum number of retries.
        '''
        self._max_retries = value

    @property
    def session(self) -> str | None:
        '''The session cookie for API requests.'''   
        return self._session

    @session.setter
    def session(self, value: str | None) -> None:
        '''Sets the session cookie for API requests.

        Args:
            value (str | None): The session cookie value.
        '''
        self._session = value

    def login(self) -> None:
        '''Logs into the XUI API and sets the session cookie.'''   
        endpoint = "login"
        headers: dict[str, str] = {}

        url = self._url(endpoint)
        data = {"username": self.username, "password": self.password}
        logger.info("Logging in with username: %s", self.username)

        response = self._post(url, headers, data)
        cookie: str | None = response.cookies.get("session")
        if not cookie:
            raise ValueError("No session cookie found, something wrong with the login...")
        logger.info("Session cookie successfully retrieved for username: %s", self.username)
        self.session = cookie

    def _check_response(self, response: requests.Response) -> None:
        '''Checks the API response for success status.'''   
        response_json = response.json()

        status = response_json.get(ApiFields.SUCCESS)
        message = response_json.get(ApiFields.MSG)
        if not status:
            raise ValueError(f"Response status is not successful, message: {message}")

    def _url(self, endpoint: str) -> str:
        '''Generates the full URL for the given endpoint.'''   
        return f"{self._host}/{endpoint}"

    def _request_with_retry(self, method: Callable[..., requests.Response], url: str, headers: dict[str, str], **kwargs: Any) -> requests.Response:
        '''Sends a request with retry logic.'''   
        logger.debug("%%s request to %%s...", method.__name__.upper(), url)
        for retry in range(1, self.max_retries + 1):
            try:
                skip_check = kwargs.pop("skip_check", False)
                response = method(url, cookies={"session": self.session}, headers=headers, **kwargs)
                response.raise_for_status()
                if skip_check:
                    return response
                self._check_response(response)
                return response
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if retry == self.max_retries:
                    raise e
                logger.warning("Request to %%s failed: %%s, retry %%s of %%s", url, e, retry, self.max_retries)
                sleep(1 * (retry + 1))
            except requests.exceptions.RequestException as e:
                raise e
        raise requests.exceptions.RetryError(f"Max retries exceeded with no successful response to {url}")

    def _post(self, url: str, headers: dict[str, str], data: dict[str, Any], **kwargs) -> requests.Response:
        '''Sends a POST request.'''   
        return self._request_with_retry(requests.post, url, headers, json=data, **kwargs)

    def _get(self, url: str, headers: dict[str, str], **kwargs) -> requests.Response:
        '''Sends a GET request.'''   
        return self._request_with_retry(requests.get, url, headers, **kwargs)
