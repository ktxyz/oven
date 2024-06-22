from typing import Optional

from oven.oven.trans import Translator


FILTER_NAME = 'gettext'


def custom_filter(msgid: str, msgstr: Optional[str] = '', lang: Optional[str] = 'en') -> str:
    trans = Translator()

    if trans.config.is_gather_config():
        trans.add_text(msgid, msgstr)
        return ''
    return trans.get_text(msgid, lang)
