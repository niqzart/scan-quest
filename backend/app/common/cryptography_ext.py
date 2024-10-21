from secrets import token_urlsafe


def generate_secure_code(length: int) -> str:
    return token_urlsafe(nbytes=length)[:length]
