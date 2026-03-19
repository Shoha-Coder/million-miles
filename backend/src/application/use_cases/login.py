import bcrypt

from src.domain.exceptions import InvalidCredentials


class Login:
    def __init__(
        self,
        valid_username: str,
        valid_password_hash: str,
        extra_username: str = "",
        extra_password_hash: str = "",
    ) -> None:
        # Build the credential table at startup — extra entry is optional
        self._credentials: list[tuple[str, bytes]] = [
            (valid_username, valid_password_hash.encode()),
        ]
        if extra_username and extra_password_hash:
            self._credentials.append((extra_username, extra_password_hash.encode()))

    async def execute(self, username: str, password: str) -> str:
        encoded = password.encode()
        for stored_username, stored_hash in self._credentials:
            # checkpw does constant-time comparison — safe against timing attacks
            if username == stored_username and bcrypt.checkpw(encoded, stored_hash):
                return username
        raise InvalidCredentials()
