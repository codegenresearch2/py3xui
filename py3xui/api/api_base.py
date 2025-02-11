from __future__ import annotations
from typing import Any, Callable
import requests
from py3xui.utils import Logger

logger = Logger(__name__)


class ApiFields:
    """Stores the fields returned by the XUI API for parsing."""

    SUCCESS = "success"
    MSG = "msg"
    OBJ = "obj"
    CLIENT_STATS = "clientStats"
    NO_IP_RECORD = "No IP Record"


class BaseApi:
    """A base class for interacting with the XUI API.

    Args:
        host (str): The base URL of the XUI API.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Attributes:
        _host (str): The base URL of the XUI API.
        _username (str): The username for authentication.
        _password (str): The password for authentication.
        _max_retries (int): The maximum number of retry attempts for API requests.
        _session (str | None): The session cookie for API requests.

    Methods:
        login: Logs into the XUI API and sets the session cookie.
        _check_response: Checks the response from the API for success status.
        _url: Constructs the full URL for an API endpoint.
        _request_with_retry: Sends a request with retry logic.
        _post: Sends a POST request with retry logic.
        _get: Sends a GET request with retry logic.
    """

    def __init__(self, host: str, username: str, password: str):
        """Initializes the BaseApi instance.

        Args:
            host (str): The base URL of the XUI API.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self._host = host.rstrip("/")
        self._username = username
        self._password = password
        self._max_retries: int = 3
        self._session: str | None = None

    @property
    def host(self) -> str:
        """The base URL of the XUI API.

        Returns:
            str: The base URL of the XUI API.
        """
        return self._host

    @property
    def username(self) -> str:
        """The username for authentication.

        Returns:
            str: The username for authentication.
        """
        return self._username

    @property
    def password(self) -> str:
        """The password for authentication.

        Returns:
            str: The password for authentication.
        """
        return self._password

    @property
    def max_retries(self) -> int:
        """The maximum number of retry attempts for API requests.

        Returns:
            int: The maximum number of retry attempts for API requests.
        """
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        """Sets the maximum number of retry attempts for API requests.

        Args:
            value (int): The new maximum number of retry attempts.
        """
        self._max_retries = value

    @property
    def session(self) -> str | None:
        """The session cookie for API requests.

        Returns:
            str | None: The session cookie for API requests.
        """
        return self._session

    @session.setter
    def session(self, value: str | None) -> None:
        """Sets the session cookie for API requests.

        Args:
            value (str | None): The session cookie for API requests.
        """
        self._session = value

    def login(self) -> None:
        """Logs into the XUI API and sets the session cookie.

        Raises:
            ValueError: If no session cookie is found after login.
        """
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
        """Checks the response from the API for success status.

        Args:
            response (requests.Response): The response from the API.

        Raises:
            ValueError: If the response status is not successful.
        """
        response_json = response.json()

        status = response_json.get(ApiFields.SUCCESS)
        message = response_json.get(ApiFields.MSG)
        if not status:
            raise ValueError(f"Response status is not successful, message: {message}")

    def _url(self, endpoint: str) -> str:
        """Constructs the full URL for an API endpoint.

        Args:
            endpoint (str): The API endpoint.

        Returns:
            str: The full URL for the API endpoint.
        """
        return f"{self._host}/{endpoint}"

    def _request_with_retry(
        self,
        method: Callable[..., requests.Response],
        url: str,
        headers: dict[str, str],
        **kwargs: Any,
    ) -> requests.Response:
        """Sends a request with retry logic.

        Args:
            method (Callable[..., requests.Response]): The HTTP method to use.
            url (str): The URL to send the request to.
            headers (dict[str, str]): The headers to include in the request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The response from the API.

        Raises:
            requests.exceptions.ConnectionError: If the connection to the API fails.
            requests.exceptions.Timeout: If the request times out.
            requests.exceptions.RequestException: For other request errors.
        """
        logger.debug("%s request to %s...", method.__name__.upper(), url)
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
                logger.warning(
                    "Request to %s failed: %s, retry %s of %s", url, e, retry, self.max_retries
                )
                sleep(1 * (retry + 1))
            except requests.exceptions.RequestException as e:
                raise e
        raise requests.exceptions.RetryError(
            f"Max retries exceeded with no successful response to {url}"
        )

    def _post(
        self, url: str, headers: dict[str, str], data: dict[str, Any], **kwargs: Any
    ) -> requests.Response:
        """Sends a POST request with retry logic.

        Args:
            url (str): The URL to send the POST request to.
            headers (dict[str, str]): The headers to include in the POST request.
            data (dict[str, Any]): The data to include in the POST request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The response from the API.
        """
        return self._request_with_retry(requests.post, url, headers, json=data, **kwargs)

    def _get(self, url: str, headers: dict[str, str], **kwargs: Any) -> requests.Response:
        """Sends a GET request with retry logic.

        Args:
            url (str): The URL to send the GET request to.
            headers (dict[str, str]): The headers to include in the GET request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The response from the API.
        """
        return self._request_with_retry(requests.get, url, headers, **kwargs)