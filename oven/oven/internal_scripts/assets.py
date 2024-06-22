import os
import logging
import shutil
from typing import List
from pathlib import Path

from oven.oven.utils import EOvenScriptExecTime
from oven.oven.config import Config

SCRIPT_NAME = 'assets'
SCRIPT_EXEC_TIME = EOvenScriptExecTime.FINISH_BUILD
SCRIPT_ORDER = -100


def gather_assets(path: Path, ignore_paths: List[Path], asset_types: List[str], output_path: Path) -> int:
    os.makedirs(output_path, exist_ok=True)

    def iter_gather(current_dir: Path) -> int:
        count = 0
        for entry in current_dir.iterdir():
            if entry in ignore_paths:
                continue
            if entry.is_dir():
                count += iter_gather(entry)
            elif entry.is_file() and entry.suffix in asset_types:
                asset_relative_path = output_path / Path(str(entry.suffix)[1:]) / entry.name
                os.makedirs(asset_relative_path.parent, exist_ok=True)
                shutil.copy2(entry, asset_relative_path)
                count += 1
        return count

    return iter_gather(path)


def execute_script(config: Config, **kwargs):
    def transform_ignore_path(path: str) -> Path:
        return config.root_path / path

    ignore_paths = list(map(transform_ignore_path, kwargs.get('ignore_paths', [])))
    asset_types = kwargs.get('types', [])

    logging.info(f'[{SCRIPT_NAME}] gathering assets')
    asset_count = gather_assets(config.root_path, ignore_paths, asset_types, config.assets_path)
    logging.info(f'[{SCRIPT_NAME}] gathered {asset_count}')
