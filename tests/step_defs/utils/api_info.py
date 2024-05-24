# This class keeps track of information about the API in the local system
import requests

from http import HTTPStatus
from urllib.parse import urlsplit, SplitResult


class APIInfo(object):
    _expected_return: HTTPStatus = None
    _parsed_url: SplitResult = None
    _response_object: requests.Response = None
    _user_name: str = None

    def __init__(self, endpoint: str = None) -> None:
        self.expected_return = HTTPStatus.NOT_FOUND
        self.url = endpoint if not None else ""
        self.user_name = "default"

    @property
    def expected_return(self) -> HTTPStatus:
        return self._expected_return

    @expected_return.setter
    def expected_return(self, retval: HTTPStatus) -> None:
        self._expected_return = retval

    @property
    def response(self) -> requests.Response:
        return self._response_object

    @response.setter
    def response(self, res: requests.Response) -> None:
        self._response_object = res

    @property
    def url(self) -> str:
        if self._parsed_url is not None:
            return self._parsed_url.geturl()
        else:
            return None

    @url.setter
    def url(self, endpoint: str = "") -> None:
        if endpoint == "":
            self._parsed_url = urlsplit("https://localhost/fake/path")
        else:
            self._parsed_url = urlsplit(endpoint)

    @property
    def user_name(self) -> str:
        return self._user_name

    @user_name.setter
    def user_name(self, name: str) -> None:
        self._user_name = name
