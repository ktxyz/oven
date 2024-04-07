import json
import logging
from pathlib import Path

from argparse import Namespace

from enum import Enum

from .errors import ErrorHolder


class EConfigType(Enum):
    UNSPECIFIED = 0
    GATHER = 1
    BUILD = 2
    WATCH = 3


class Config:
    CONFIG_FILE = 'oven.json'

    def __init__(self, args: Namespace, config_type: EConfigType = EConfigType.UNSPECIFIED) -> None:
        self.root_path = Path.cwd()
        self.config_path = self.root_path / Config.CONFIG_FILE

        self.config_type = config_type

        try:
            with open(self.config_path, encoding='utf-8', mode='r') as f:
                self._raw_json = json.load(f)
        except Exception as e:
            ErrorHolder().add_error(e)

        self.site_url = self._raw_json.get('site_url', 'https://localhost:80')
        self.site_timezone = self._raw_json.get('site_timezone', 'Europe/Warsaw')

        self.source_path = self.root_path / self._raw_json.get('source_dir', 'content')
        self.build_path = self.root_path / self._raw_json.get('build_dir', 'build')

        self.theme_path = self.root_path / self._raw_json.get('theme_dir', 'theme')
        self.locales_path = self.root_path / self._raw_json.get('locales_dir', 'locales')
        self.locales_main = self._raw_json.get('locales_main', 'en')
        self.locales_langs = self._raw_json.get('locales_langs', ['en'])

        self.filters_path = self.root_path / self._raw_json.get('filters_dir', 'filters')
        self.enabled_filters = self._raw_json.get('enabled_filters', None)

        self.extensions_path = self.root_path / self._raw_json.get('extensions_dir', 'extensions')
        self.enabled_extensions = self._raw_json.get('enabled_extensions', None)

        self.scripts_path = self.root_path / self._raw_json.get('scripts_dir', 'scripts')
        if args.force_scripts:
            self.enabled_scripts = args.force_scripts.split(',')
        else:
            self.enabled_scripts = self._raw_json.get('enabled_scripts', None)
            if args.enable_scripts:
                self.enabled_scripts.extend(args.enable_scripts.split(','))
            if args.disable_scripts:
                for script in args.disabled_scripts.split(','):
                    self.enabled_scripts.remove(script)

        self.scripts_config = self._raw_json.get('scripts_config', {})

        self.default_template_name = self._raw_json.get('default_template_name', 'page.html')

        logging.info(f'[Config] loaded from {self.config_path}')

    def is_build_config(self) -> bool:
        return self.config_type == EConfigType.BUILD

    def is_gather_config(self) -> bool:
        return self.config_type == EConfigType.GATHER
