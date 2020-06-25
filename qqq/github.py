from typing import Union, Dict

import requests
from requests.auth import HTTPBasicAuth


class GitHub:
    _api_base_url = 'https://api.github.com'

    def __init__(self, username, token):
        self.username = username
        self.token = token

    @classmethod
    def verify_token(cls, username: str, token: str) -> bool:
        """
        Verify a GitHub personal access token.

        :param username: The GitHub user associated with the token
        :param token: The personal access token
        :return:
        """
        r = requests.get('https://api.github.com/user', auth=HTTPBasicAuth(username, token))
        return r.status_code == 200

    def get_user(self, username: str) -> Union[Dict, None]:
        """
        Get a GitHub user.

        :param username: The user to get from GitHub.
        :return: JSON response from GitHub API if the user exists
        """
        r = requests.get(f'{self._api_base_url}/users/{username}')
        return r.json() if r.status_code == 200 else None

    def create_repo(self, name: str) -> Union[Dict, None]:
        """
        Create a private repo on GitHub.

        :param name: The name of the repo
        :return: JSON response from GitHub API if the request was successful
        """
        r = requests.post(
            f'{self._api_base_url}/user/repos',
            json={'name': name, 'private': True},
            auth=HTTPBasicAuth(self.username, self.token)
        )
        return r.json() if r.status_code == 201 else None

    def add_collaborator(self, repo_name: str, username: str, admin: bool = False) -> bool:
        """
        Add a collaborator to a GitHub repo.

        :param repo_name: The name of the repo on GitHub
        :param username: The username of the collaborator
        :param admin: Whether or not the collaborator should have admin privileges
        :return: True if the request was successful
        """
        r = requests.put(
            f'{self._api_base_url}/repos/{self.username}/{repo_name}/collaborators/{username}',
            auth=HTTPBasicAuth(self.username, self.token),
            json={'permission': 'admin'} if admin else None
        )
        return r.status_code in (201, 204)
