from typing import Optional

from oven.urls import URLArchive

FILTER_NAME = 'geturl'


def custom_filter(name: str, lang: Optional[str] = 'en') -> str:
    return URLArchive().get_url(name, lang)
