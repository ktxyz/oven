import logging

from oven.oven.utils import EOvenScriptExecTime
from oven.oven.config import Config

SCRIPT_NAME = 'robots.txt'
SCRIPT_EXEC_TIME = EOvenScriptExecTime.FINISH_BUILD
SCRIPT_ORDER = 0


def execute_script(config: Config, **kwargs) -> None:
    output_file = 'robots.txt'
    if 'output_file' in kwargs:
        output_file = kwargs['output_file']

    logging.info(f'[{SCRIPT_NAME}] generating {output_file} file')
    with open(config.build_path / output_file, 'w') as f:
        f.write('')
