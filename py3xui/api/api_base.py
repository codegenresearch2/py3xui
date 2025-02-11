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
    """A class to interact with the XUI API.

    Args:
        host (str): The XUI host URL.
        username (str): The XUI username.
        password (str): The XUI password.

    Attributes:
        _host (str): The XUI host URL (read-only).
        _username (str): The XUI username (read-only).
        _password (str): The XUI password (read-only).
        _max_retries (int): The maximum number of retry attempts for requests.
        _session (str | None): The session cookie for API requests.

    Public Methods:
        login: Logs into the XUI API.
        _url: Constructs the full URL for the given endpoint.
        _request_with_retry: Sends a request with retry logic.
        _post: Sends a POST request with retry logic.
        _get: Sends a GET request with retry logic.
    """

    def __init__(self, host: str, username: str, password: str):
        self._host = host.rstrip("/")
        self._username = username
        self._password = password
        self._max_retries: int = 3
        self._session: str | None = None

    @property
    def host(self) -> str:
        """The XUI host URL.

        Returns:
            str: The host URL.
        """
        return self._host

    @property
    def username(self) -> str:
        """The XUI username.

        Returns:
            str: The username.
        """
        return self._username

    @property
    def password(self) -> str:
        """The XUI password.

        Returns:
            str: The password.
        """
        return self._password

    @property
    def max_retries(self) -> int:
        """The maximum number of retry attempts for requests.

        Returns:
            int: The maximum retries.
        """
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        """Sets the maximum number of retry attempts for requests.

        Args:
            value (int): The new maximum retries value.
        """
        self._max_retries = value

    @property
    def session(self) -> str | None:
        """The session cookie for API requests.

        Returns:
            str | None: The session cookie, or None if not set.
        """
        return self._session

    @session.setter
    def session(self, value: str | None) -> None:
        """Sets the session cookie for API requests.

        Args:
            value (str | None): The session cookie to set.
        """
        self._session = value

    def login(self) -> None:
        """Logs into the XUI API and sets the session cookie.

        This method sends a login request to the XUI API using the provided username and password.
        It retrieves the session cookie from the response and stores it for future requests.

        Raises:
            ValueError: If no session cookie is found in the response.
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

    def _url(self, endpoint: str) -> str:
        """Constructs the full URL for the given endpoint.

        Args:
            endpoint (str): The API endpoint.

        Returns:
            str: The full URL.
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

        This method attempts to send a request using the provided method, URL, headers, and keyword arguments.
        It retries the request up to a specified number of times if a connection or timeout error occurs.

        Args:
            method (Callable[..., requests.Response]): The HTTP method to use (e.g., requests.post).
            url (str): The URL to send the request to.
            headers (dict[str, str]): The headers to include in the request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The response from the request.

        Raises:
            requests.exceptions.ConnectionError: If a connection error occurs.
            requests.exceptions.Timeout: If a timeout error occurs.
            requests.exceptions.RequestException: For other request-related exceptions.
            ValueError: If the response status is not successful.
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
        self, url: str, headers: dict[str, str], data: dict[str, Any], **kwargs
    ) -> requests.Response:
        """Sends a POST request with retry logic.

        This method sends a POST request to the specified URL with the provided headers and data.

        Args:
            url (str): The URL to send the POST request to.
            headers (dict[str, str]): The headers to include in the request.
            data (dict[str, Any]): The data to include in the request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The response from the POST request.
        """
        return self._request_with_retry(requests.post, url, headers, json=data, **kwargs)

    def _get(self, url: str, headers: dict[str, str], **kwargs) -> requests.Response:
        """Sends a GET request with retry logic.

        This method sends a GET request to the specified URL with the provided headers.

        Args:
            url (str): The URL to send the GET request to.
            headers (dict[str, str]): The headers to include in the request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The response from the GET request.
        """
        return self._request_with_retry(requests.get, url, headers, **kwargs)

    def _check_response(self, response: requests.Response) -> None:
        """Checks the response using the success field.

        This method checks the response JSON for the success field and raises a ValueError if the response is not successful.

        Args:
            response (requests.Response): The HTTP response.

        Raises:
            ValueError: If the response status is not successful.
        """
        response_json = response.json()

        status = response_json.get(ApiFields.SUCCESS)
        message = response_json.get(ApiFields.MSG)
        if not status:
            raise ValueError(f"Response status is not successful, message: {message}")