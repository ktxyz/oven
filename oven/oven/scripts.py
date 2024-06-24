import time
import logging
from types import FunctionType, ModuleType
from pathlib import Path

from importlib import resources

from .utils import EOvenScriptExecTime
from .config import Config

from .utils import load_module

INTERNAL_SCRIPTS_PACKAGE = 'oven.oven.internal_scripts'


def is_valid_script(module: ModuleType) -> bool:
    return hasattr(module, 'SCRIPT_NAME') and hasattr(module, 'SCRIPT_EXEC_TIME') and hasattr(module, 'SCRIPT_ORDER') and hasattr(module, 'execute_script')


class ScriptsManager:
    class Script:
        def __init__(self, name: str, function: FunctionType, exec_time: EOvenScriptExecTime, order: int) -> None:
            self.name = name
            self.function = function
            self.exec_time = exec_time
            self.order = order

        def execute(self, config: Config, **kwargs) -> None:
            self.function(config, **kwargs)

    _instance = None

    def __init__(self, config: Config) -> None:
        self.config = config
        self.scripts = []

        self.__load_scripts(INTERNAL_SCRIPTS_PACKAGE, True)
        self.__load_scripts(self.config.scripts_path)
        self.scripts.sort(key=lambda script: script.order)

    def __load_modules(self, path: Path, internal: bool = False):
        modules = []
        for script_name in map(str, path.iterdir()) if not internal else resources.contents(INTERNAL_SCRIPTS_PACKAGE):
            if script_name.endswith('.py'):
                if internal:
                    with resources.path(INTERNAL_SCRIPTS_PACKAGE, script_name) as script_path:
                        modules.append(load_module('oven_script', script_path)) 
                else:
                    modules.append(load_module('oven_script', script_name))
        return modules 

    def __load_scripts(self, path: Path, internal: bool = False) -> None:
        if not (internal or path.exists()):
            return
        loaded_scripts = 0

        logging.info(f'[Scripts] Loading scripts from {path if not internal else "INTERNAL"}')
        for module in self.__load_modules(path, internal):
            if is_valid_script(module):
                if not self.config.enabled_scripts or module.SCRIPT_NAME in self.config.enabled_scripts:
                    logging.info(f'[Scripts] loaded script: {module.SCRIPT_NAME} with order: {module.SCRIPT_ORDER}')
                    loaded_scripts += 1
                    self.scripts.append(
                        ScriptsManager.Script(module.SCRIPT_NAME, module.execute_script, module.SCRIPT_EXEC_TIME,
                                              module.SCRIPT_ORDER))
        logging.info(f'[Scripts] Loaded {loaded_scripts} scripts')

    def execute(self, exec_time: EOvenScriptExecTime) -> None:
        for script in self.scripts:
            if script.exec_time == exec_time:
                _start_time = time.time()
                script.execute(self.config, **self.config.scripts_config.get(script.name, {}))
                logging.info(f'[Scripts] script {script.name} took {time.time() - _start_time:.3f}s')
