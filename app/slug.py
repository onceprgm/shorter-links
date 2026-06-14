import secrets
import string

from app.config import settings

_ALPHABET = string.ascii_letters + string.digits


def generate_slug(length: int | None = None) -> str:
    n = length or settings.slug_length
    return "".join(secrets.choice(_ALPHABET) for _ in range(n))
