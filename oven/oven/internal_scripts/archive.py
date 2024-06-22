import os
import zipfile
import logging
import shutil
import datetime
from typing import List
from pathlib import Path

from oven.oven.utils import EOvenScriptExecTime
from oven.oven.config import Config

SCRIPT_NAME = 'archive'
SCRIPT_EXEC_TIME = EOvenScriptExecTime.START_BUILD
SCRIPT_ORDER = -100


def archive_build_zip(path: Path, ignore_paths: List[Path], output_path: Path, ) -> None:
    os.makedirs(output_path.parent, exist_ok=True)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        def iter_zip(current_dir: Path):
            for entry in current_dir.iterdir():
                if entry in ignore_paths:
                    continue
                if entry.is_dir():
                    iter_zip(entry)
                elif entry.is_file():
                    relative_path = entry.relative_to(path)
                    zip_file.write(entry, relative_path)

        iter_zip(path)


def archive_build_raw(path, ignore_paths: List[Path], output_path: Path) -> None:
    os.makedirs(output_path, exist_ok=True)

    def iter_copy(current_dir: Path):
        for entry in current_dir.iterdir():
            if entry in ignore_paths:
                continue
            if entry.is_dir():
                iter_copy(entry)
            elif entry.is_file():
                relative_path = output_path / entry.relative_to(path)
                os.makedirs(relative_path.parent, exist_ok=True)
                shutil.copy(entry, relative_path)

    iter_copy(path)


def execute_script(config: Config, **kwargs):
    archive_name = str(datetime.datetime.now().strftime("%Y-%M-%D %H-%M-%S")).replace('/', '_').replace(' ', '_')

    generate_zip = kwargs.get('generate_zip', True)
    zip_path = config.root_path / kwargs.get('zip_dir', '_archive') / (archive_name + '.zip')

    generate_raw = kwargs.get('generate_raw')
    raw_path = config.build_path / kwargs.get('raw_dir', '_archive') / archive_name

    def transform_ignore_path(path: str) -> Path:
        return config.build_path / path
    ignore_paths = list(map(transform_ignore_path, kwargs.get('ignore_paths', [])))

    if generate_zip:
        logging.info(f'[{SCRIPT_NAME}] Creating archive {zip_path}')
        archive_build_zip(config.build_path, ignore_paths, zip_path)

    if generate_raw:
        logging.info(f'[{SCRIPT_NAME}] Creating archive {raw_path}')
        archive_build_raw(config.build_path, ignore_paths, raw_path)
