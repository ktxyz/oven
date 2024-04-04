from typing import Dict, Optional, List

from markdown import Markdown
from jinja2 import Environment, FileSystemLoader

from .config import Config
from .trans import Translator


def gettext_filter(msgid: str, msgstr: Optional[str] = '', lang: Optional[str] = 'en') -> str:
    trans = Translator()

    if trans.config.is_gather_config():
        trans.add_text(msgid, msgstr)
        return ''
    return trans.get_text(msgid, lang)


class Theme:
    _instance = None

    def __new__(cls, config: Optional[Config] = None):
        if cls._instance is None:
            cls._instance = super(Theme, cls).__new__(cls)
            cls._instance.__initialize(config)
        return cls._instance

    def __initialize(self, config: Config) -> None:
        self.config = config
        self.env = Environment(loader=FileSystemLoader(self.config.theme_path), autoescape=True)
        self.env.filters['gettext'] = gettext_filter

        if self.config.is_build_config():
            self.markdown = Markdown(extensions=self.config.markdown_extensions)

        if self.config.is_gather_config():
            self.__render_dummy_templates()

    def __render_dummy_templates(self) -> None:
        for template_name in self.env.list_templates():
            template = self.env.get_template(template_name)
            template.render()

    def render(self, template_name: str, contents: Optional[dict] = None, context: Optional[Dict] = None) -> str:
        template = self.env.get_template(template_name)

        if contents is None:
            contents = {}
        for key, text in contents.items():
            contents[key] = self.markdown.convert(text)

        return template.render({**contents, **{**context, 'config': self.config}})
