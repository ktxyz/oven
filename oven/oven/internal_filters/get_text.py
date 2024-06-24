from typing import Optional

from oven.oven.trans import Translator
from oven.oven.config import Config


FILTER_NAME = 'gettext'


def custom_filter(msgid: str, lang: Optional[str] = 'en', should_gather: bool = True, msgstr: Optional[str] = '') -> str:
    trans = Translator()

    if trans.config.is_gather_config():
        if should_gather:
            if Config().get_active_node():
                trans.add_text(f'{Config().get_active_node()}-{msgid}', msgstr)
            else:
                trans.add_text(msgid, msgstr)
            return ''
    return trans.get_text(f'{Config().get_active_node()}-{msgid}', lang)
