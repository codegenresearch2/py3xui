from typing import Any, Callable
import requests
from py3xui.utils import Logger

logger = Logger(__name__)


# pylint: disable=too-few-public-methods
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
        _max_retries (int): The maximum number of retries for API requests.
        _session (str | None): The session cookie for API requests.
    """

    def __init__(self, host: str, username: str, password: str):
        """Initializes the BaseApi instance.

        Args:
            host (str): The XUI host URL.
            username (str): The XUI username.
            password (str): The XUI password.
        """
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
        """The maximum number of retries for API requests.

        Returns:
            int: The maximum retries.
        """
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        """Sets the maximum number of retries for API requests.

        Args:
            value (int): The new maximum retries value.
        """
        self._max_retries = value

    @property
    def session(self) -> str | None:
        """The session cookie for API requests.

        Returns:
            str | None: The session cookie.
        """
        return self._session

    @session.setter
    def session(self, value: str | None) -> None:
        """Sets the session cookie for API requests.

        Args:
            value (str | None): The session cookie value.
        """
        self._session = value

    def login(self) -> None:
        """Logs into the XUI API and sets the session cookie.

        Raises:
            ValueError: If the login is unsuccessful.
        """
        endpoint = "login"
        headers: dict[str, str] = {}

        url = self._url(endpoint)
        data = {"username": self.username, "password": self.password}
        logger.info("Logging in with username: %s", self.username)

        response = self._post(url, headers, data)
        cookie: str | None = response.cookies.get("session")
        if not cookie:
            raise ValueError("Login failed, no session cookie found.")
        logger.info("Session cookie successfully retrieved for username: %s", self.username)
        self.session = cookie

    def _check_response(self, response: requests.Response) -> None:
        """Checks the response from the API for success status.

        Args:
            response (requests.Response): The API response.

        Raises:
            ValueError: If the response status is not successful.
        """
        response_json = response.json()

        status = response_json.get(ApiFields.SUCCESS)
        message = response_json.get(ApiFields.MSG)
        if not status:
            raise ValueError(f"Response status is not successful, message: {message}")

    def _url(self, endpoint: str) -> str:
        """Constructs the full URL for API endpoints.

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
        """Makes a request to the XUI API with retries.

        Args:
            method (Callable[..., requests.Response]): The HTTP method to use.
            url (str): The URL to request.
            headers (dict[str, str]): The headers to include in the request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The API response.

        Raises:
            requests.exceptions.ConnectionError: If the connection fails.
            requests.exceptions.Timeout: If the request times out.
            requests.exceptions.RequestException: For other request errors.
            requests.exceptions.RetryError: If all retries fail.
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
        """Sends a POST request to the XUI API.

        Args:
            url (str): The URL to request.
            headers (dict[str, str]): The headers to include in the request.
            data (dict[str, Any]): The data to send in the request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The API response.
        """
        return self._request_with_retry(requests.post, url, headers, json=data, **kwargs)

    def _get(self, url: str, headers: dict[str, str], **kwargs: Any) -> requests.Response:
        """Sends a GET request to the XUI API.

        Args:
            url (str): The URL to request.
            headers (dict[str, str]): The headers to include in the request.
            **kwargs (Any): Additional keyword arguments to pass to the request method.

        Returns:
            requests.Response: The API response.
        """
        return self._request_with_retry(requests.get, url, headers, **kwargs)