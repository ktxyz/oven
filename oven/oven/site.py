import json
import logging

from typing import List
from pathlib import Path

from .config import Config
from .trans import Translator


class Content:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.stem
        self.msg_id = path.parent.stem + '-' + self.name

        logging.info(f'[Content][{self.name}] loading default data')

        with open(self.path, 'r') as f:
            self.default_data = f.read()
        self.trans = {}

    def get_lang(self, lang: str) -> str:
        return self.trans.get(lang, self.default_data)

    def add_lang(self, lang: str, data: str) -> None:
        logging.info(f'[Content][{self.name}] adding {lang} lang')
        self.trans[lang] = data

    def __str__(self) -> str:
        return f'[Content][{self.name}][{self.msg_id}] = {self.default_data}'


class Node:
    CONFIG_FILE = "config.json"
    CONTEXT_FILE = "context.json"

    def __init__(self, path: Path, config: Config) -> None:
        self.config = config
        self.path = path
        self.name = self.path.stem

        self.contents = []
        self.context = {}
        self._raw_config = {}

        logging.info(f'[Node][{self.name}] detected at {self.path}')
        self.__load_content()
        if self.config.is_build_config():
            self.__load_config()
            self.__load_context()

    def __load_context(self):
        logging.info(f'[Node][{self.name}] loading context')

        try:
            with open(self.path / Node.CONTEXT_FILE, encoding='utf-8', mode='r') as f:
                self.context = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f'[Node][{self.name}] error {e}')

    def __load_content(self) -> None:
        logging.info(f'[Node][{self.name}] loading content')

        for file in self.path.iterdir():
            if file.is_file() and file.suffix == ".md":
                self.contents.append(Content(file))

    def __load_config(self) -> None:
        logging.info(f'[Node][{self.name}] loading config')

        try:
            with open(self.path / self.CONFIG_FILE, encoding='utf-8', mode='r') as f:
                self._raw_config = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f'[Node][{self.name}] error {e}')

        self.output_name = self._raw_config.get("output_name", self.path.stem)

    def load_translations(self, trans: Translator) -> None:
        logging.info(f'[Node][{self.name}] loading translations')

        for lang in self.config.locales_langs:
            for content in self.contents:
                content.add_translation(lang, trans.get_text(content.msg_id, lang))

    def get_contents(self) -> List[Content]:
        return self.contents


class Site:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.nodes = []

        self.__gather_nodes()
        logging.info(f'[Site] gathered {len(self.nodes)} nodes')

        if self.config.is_build_config():
            self.__load_translations()
        elif self.config.is_gather_config():
            self.__gather_translations()

    def __gather_nodes(self) -> None:
        logging.info(f'[Site] Gathering nodes')

        for file in self.config.source_path.iterdir():
            if file.is_dir():
                self.nodes.append(Node(file, self.config))

    def __load_translations(self) -> None:
        for node in self.nodes:
            node.load_translations(Translator())

    def __gather_translations(self) -> None:
        for node in self.nodes:
            for content in node.get_contents():
                Translator().add_text(content.msg_id, content.default_data)
