from urllib.parse import urlparse, urlunparse

from app.config import settings


def normalize_url(raw: str) -> str | None:
    # Accept http/https; prepend https:// when no scheme is given. Return None if invalid
    raw = raw.strip()
    if not raw:
        return None

    parsed = urlparse(raw)
    if not parsed.scheme:
        parsed = urlparse("https://" + raw)

    if parsed.scheme not in ("http", "https"):
        return None
    if not parsed.netloc or "." not in parsed.netloc:
        return None

    return urlunparse(parsed)


def short_link(slug: str) -> str:
    return f"https://t.me/{settings.bot_username}?start={slug}"
