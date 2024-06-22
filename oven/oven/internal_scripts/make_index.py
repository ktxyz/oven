import logging
import shutil

from oven.oven.utils import EOvenScriptExecTime
from oven.oven.config import Config

SCRIPT_NAME = 'make_index'
SCRIPT_EXEC_TIME = EOvenScriptExecTime.FINISH_BUILD
SCRIPT_ORDER = 100


def execute_script(config: Config, **kwargs) -> None:
    index_output_page = kwargs.get('index_output_name', 'index')

    logging.info(f'[{SCRIPT_NAME}] copying {index_output_page} as index.html')
    try:
        shutil.copyfile(config.build_path / index_output_page / 'index.html', config.build_path / 'index.html')
    except FileNotFoundError:
        logging.error(f'File {index_output_page}/index.html not found, make sure configuration is correct')
