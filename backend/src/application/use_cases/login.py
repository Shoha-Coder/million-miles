from src.domain.exceptions import InvalidCredentials


class Login:
    def __init__(self, valid_username: str, valid_password: str) -> None:
        self._username = valid_username
        self._password = valid_password

    async def execute(self, username: str, password: str) -> None:
        if username != self._username or password != self._password:
            raise InvalidCredentials()
