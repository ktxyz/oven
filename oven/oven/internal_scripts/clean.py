import os

import logging

from typing import List
from pathlib import Path

from oven.oven.utils import EOvenScriptExecTime
from oven.oven.config import Config

SCRIPT_NAME = 'clean'
SCRIPT_EXEC_TIME = EOvenScriptExecTime.START_BUILD
SCRIPT_ORDER = 100


def clean_build(path: Path, ignore_paths: List[str]) -> None:
    def transform_ignore_path(ignore_path: str) -> Path:
        return path / ignore_path
    ignore_paths = list(map(transform_ignore_path, ignore_paths))

    def iter_clean(current_dir: Path):
        for entry in current_dir.iterdir():
            if entry in ignore_paths:
                continue
            if entry.is_dir():
                iter_clean(entry)
                if not any(entry.iterdir()):
                    os.rmdir(entry)
            elif entry.is_file():
                os.remove(entry)

    iter_clean(path)


def execute_script(config: Config, **kwargs) -> None:
    ignore_paths = kwargs.get('ignore_paths', [])

    logging.info(f'[{SCRIPT_NAME}] cleaning build path')
    clean_build(config.build_path, ignore_paths)
