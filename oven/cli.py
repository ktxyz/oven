import time
import shutil
import logging
import argparse

from oven.config import Config, EConfigType
from oven.trans import Translator
from oven.theme import Theme
from oven.site import Site
from oven.urls import URLArchive
from oven.scripts import ScriptsManager, EOvenScriptExecTime


def build_site(args):
    logging.info("[Oven Site Build Started]")
    config = Config(args, EConfigType.BUILD)
    run(config)


def gather_trans(args):
    logging.info("[Oven Site Trans Gather Started]")
    config = Config(args, EConfigType.GATHER)
    run(config)


def run(config: Config) -> None:
    _start_time = time.time()

    # initialize singletons with config
    _ = Translator(config)
    _ = Theme(config)
    _ = URLArchive(config)

    # initialize other classes
    scripts = ScriptsManager(config)

    scripts.execute(EOvenScriptExecTime.START_BUILD if config.is_build_config() else EOvenScriptExecTime.START_GATHER)
    site = Site(config)
    if config.is_build_config():
        site.output_content()
    scripts.execute(EOvenScriptExecTime.FINISH_BUILD if config.is_build_config() else EOvenScriptExecTime.FINISH_GATHER)

    logging.info(f'[Oven Site Finished] {time.time() - _start_time:.3f}s')


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description='oven - yet another static site generator with markdown support')
    parser.add_argument('--enable-scripts', help='Comma-separated list of scripts to enable')
    parser.add_argument('--disable-scripts', help='Comma-separated list of scripts to be')
    parser.add_argument('--force-scripts', help='Comma-separated list of scripts to override config')

    subparsers = parser.add_subparsers(help='commands')

    # Build
    build_parser = subparsers.add_parser('build', help='Build static site')
    build_parser.set_defaults(func=build_site)

    # Gather
    gather_parser = subparsers.add_parser('gather', help='`Gather translations')
    gather_parser.set_defaults(func=gather_trans)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
