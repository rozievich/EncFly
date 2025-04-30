import os
from hashlib import pbkdf2_hmac


def key_from_password(password: str, salt: bytes = None, iterations: int = 100_000) -> bytes:
    if salt is None:
        salt = os.urandom(16)

    key = pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode(),
        salt=salt,
        iterations=iterations,
        dklen=32
    )
    return key, salt
