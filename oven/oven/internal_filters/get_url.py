from typing import Optional

from oven.oven.urls import URLArchive
from oven.oven.config import Config

FILTER_NAME = 'geturl'

# TODO:
#   Static url resolving is dirty, bad, unoptimized and stupid
#   Needs to be made human


def custom_filter(name: str, lang: Optional[str] = 'en') -> str:
    if name.endswith('__asset'):
        name = name.replace('__asset', '')
        extension = name.split('_')[-1]
        name = name.replace('_' + extension, '')
        return f'{Config().site_root}/{Config().assets_dir}/{extension}/{name}.{extension}'

    return URLArchive().get_url(name, lang)
