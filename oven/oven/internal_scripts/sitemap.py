import logging
from typing import List
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET

import pytz

from oven.oven.utils import EOvenScriptExecTime
from oven.oven.config import Config

SCRIPT_NAME = 'sitemap.xml'
SCRIPT_EXEC_TIME = EOvenScriptExecTime.FINISH_BUILD
SCRIPT_ORDER = 1


def parse_date(date: datetime, timezone: str) -> str:
    tz = pytz.timezone(timezone)
    return str(tz.localize(date))


def build_sitemap(path: Path, ignore_paths: List[str], url: str, timezone: str) -> ET.ElementTree:
    sitemap = ET.Element('urlset', xmlns='https://www.sitemaps.org/schemas/sitemap/0.9')

    def transform_ignore_path(ignore_path: str) -> Path:
        return path / ignore_path
    ignore_paths = list(map(transform_ignore_path, ignore_paths))

    def iter_build_sitemap(current_dir: Path):
        for entry in current_dir.iterdir():
            if entry in ignore_paths:
                continue
            elif entry.is_dir():
                iter_build_sitemap(entry)
            elif entry.is_file():
                file_url = str(entry).replace(str(path), url)

                url_element = ET.SubElement(sitemap, 'url')
                loc_element = ET.SubElement(url_element, 'loc')
                loc_element.text = file_url
                lastmod_element = ET.SubElement(url_element, 'lastmod')
                lastmod_element.text = parse_date(datetime.fromtimestamp(entry.stat().st_mtime), timezone)

    iter_build_sitemap(path)
    tree = ET.ElementTree(sitemap)
    ET.indent(tree, space='\t')
    return tree


def execute_script(config: Config, **kwargs) -> None:
    output_file = 'sitemap.xml'
    ignore_paths = kwargs.get('ignore_paths', [])

    logging.info(f'[{SCRIPT_NAME}] generating {output_file} file')
    build_sitemap(config.build_path, ignore_paths, config.site_url, config.site_timezone).write(
        config.build_path / output_file, encoding='utf-8')
