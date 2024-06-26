# This class keeps track of information about the API in the local system
import requests

from urllib.parse import urlsplit, SplitResult


class APIInfo(object):
    _auth_token: str = None
    _parsed_url: SplitResult = None
    _response_object: requests.Response = None
    _user_name: str = None

    def __init__(self, endpoint: str = None) -> None:
        self.url = endpoint if not None else ""
        self.user_name = "default"

    @property
    def auth_token(self) -> str:
        return self._auth_token
    
    @auth_token.setter
    def auth_token(self, token: str) -> None:
        self._auth_token = token

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
