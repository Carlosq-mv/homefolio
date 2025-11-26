from pwdlib import PasswordHash

class Auth:
    def __init__(self):
        self._hasher = PasswordHash.recommended()

    def hash_password(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._hasher.verify(plain_password, hashed_password)
